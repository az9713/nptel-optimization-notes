"""Compare public served files to Git, excluding this receipt's own bytes."""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = 'validation/publication-checks.json'


def main(base_url):
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').split('\0')
    paths = [name for name in tracked if name and not name.startswith('.')
             and name != RECEIPT and name != 'README.txt']

    def fetch(relative):
        expected = subprocess.check_output(['git', 'show', f'{commit}:{relative}'], cwd=ROOT)
        url = base_url.rstrip('/') + '/' + quote(relative) + '?release=' + commit
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Optimization-study-edition-validation'})
            with urllib.request.urlopen(request, timeout=40) as response:
                actual = response.read()
            return dict(file=relative, bytes_match_git=actual == expected,
                        sha256=hashlib.sha256(expected).hexdigest(), bytes=len(expected))
        except (urllib.error.URLError, TimeoutError) as exc:
            return dict(file=relative, bytes_match_git=False, error=str(exc))

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(fetch, paths))
    failures = [r for r in results if not r['bytes_match_git']]
    report = dict(status='pass' if not failures else 'fail', checked_commit=commit,
                  base_url=base_url, served_files=results, failure_count=len(failures),
                  excluded_self=RECEIPT,
                  scope='Compares listed served files with the checked Git tree; this receipt does not hash itself. Scientific acceptance and browser checks are separate.')
    (ROOT / RECEIPT).write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(status=report['status'], checked_commit=commit,
                          served_files=len(results), failures=failures), indent=2))
    return bool(failures)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base_url')
    raise SystemExit(main(parser.parse_args().base_url))
