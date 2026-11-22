"""Verify independent acceptance receipts and a source-free reproducible build."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    errors, receipts, accepted = [], [], {}
    for receipt in sorted((ROOT / 'validation').glob('*.json')):
        if 'review' not in receipt.stem:
            continue
        row = json.loads(receipt.read_text(encoding='utf-8-sig'))
        mapping = row.get('accepted_files', {})
        if not mapping:
            continue
        if row.get('remaining_findings'):
            errors.append(f'{receipt.name}: unresolved findings')
        for relative, value in mapping.items():
            path = (ROOT / relative).resolve()
            if not path.is_relative_to(ROOT):
                errors.append(f'{receipt.name}: accepted path leaves package')
                continue
            if not path.exists() or digest(path) != value:
                errors.append(f'{receipt.name}: stale accepted digest for {relative}')
            accepted[relative] = value
        receipts.append(receipt.name)
    for number in range(1, 17):
        for relative in [f'chapters/ch{number:02d}.md', f'chapters/ch{number:02d}.json', f'labs/ch{number:02d}.py']:
            if relative not in accepted:
                errors.append(f'{relative}: no independent acceptance receipt')
    baseline = {p.name: digest(p) for p in ROOT.glob('*.html')}
    baseline['book.json'] = digest(ROOT / 'book.json')
    (ROOT / 'work').mkdir(exist_ok=True)
    # Only authoring inputs and public assets enter the rebuild. No work/ sources.
    with tempfile.TemporaryDirectory(prefix='optimization-export-', dir=ROOT / 'work') as temp:
        target = Path(temp)
        for name in ['chapters', 'labs', 'assets', 'tools']:
            shutil.copytree(ROOT / name, target / name, ignore=shutil.ignore_patterns('__pycache__'))
        for name in ['source-manifest.json', 'overview.md', 'study-guide.md', 'references.md', 'numerical-lab.md']:
            shutil.copyfile(ROOT / name, target / name)
        environment = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
        result = subprocess.run([sys.executable, str(target / 'tools' / 'build.py')],
                                cwd=target, capture_output=True, text=True,
                                timeout=180, env=environment)
        if result.returncode:
            errors.append('Source-free rebuild failed: ' + result.stderr[-1000:])
        rebuilt = {}
        for name, expected in baseline.items():
            path = target / name
            rebuilt[name] = path.exists() and digest(path) == expected
            if not rebuilt[name]:
                errors.append(f'{name}: source-free rebuild differs')
    report = dict(status='pass' if not errors else 'fail', independent_review_receipts=receipts,
                  accepted_file_count=len(accepted), source_free_byte_identical=rebuilt,
                  errors=errors, scope='Receipt freshness and reproducibility, not new scientific review.')
    (ROOT / 'validation' / 'release-checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
