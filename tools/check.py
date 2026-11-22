"""Validate the study edition without using private source material."""
import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import os
import re
import runpy
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

# Every file is explicitly decoded as UTF-8, so byte detection is unnecessary.
sys.modules.setdefault('chardet', None)
sys.modules.setdefault('cchardet', None)
sys.modules.setdefault('charset_normalizer', None)
sys.modules.setdefault('lxml', None)
sys.modules.setdefault('html5lib', None)
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [[1, 2, 3], [4, 5, 6, 7], [8, 9, 10], [11, 12], [13, 14, 15],
            [16, 17, 18], [19, 20], [21, 22], [23, 24], [25, 26, 27, 28],
            [29, 30, 31], [32, 33], [34], [35, 36], [37, 38], [39, 40]]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(allow_partial=False, shared_process=False):
    errors, labs, chapters, link_count = [], [], [], 0
    manifest = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
    recordings = {r['video_id']: r for r in manifest['recordings']}
    if len(recordings) != 40:
        errors.append('Expected exactly 40 source recordings')
    positions = sorted(r['playlist_position'] for r in recordings.values())
    if positions != list(range(1, 41)):
        errors.append('Playlist positions are incomplete or duplicated')
    covered = []
    for meta in sorted((ROOT / 'chapters').glob('ch[0-9][0-9].json')):
        chapter = json.loads(meta.read_text(encoding='utf-8-sig'))
        number = int(meta.stem[2:])
        if chapter['lectures'] != EXPECTED[number-1]:
            errors.append(f'{meta.name}: incorrect lecture assignment')
        covered.extend(chapter['lectures'])
        source = meta.with_suffix('.md')
        page = ROOT / f'{meta.stem}.html'
        lab = ROOT / 'labs' / f'{meta.stem}.py'
        if not source.exists() or not page.exists() or not lab.exists():
            errors.append(f'{meta.stem}: missing source, page or lab')
            continue
        text = source.read_text(encoding='utf-8')
        if re.search(r'\[(?:PROOF NEEDED|CITATION NEEDED|TODO|NUMBER NOT YET COMPUTED)', text):
            errors.append(f'{source.name}: unfinished placeholder')
        soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        article = soup.select_one('article')
        details = article.select('details') if article else []
        exercise_headings = re.findall(r'(?im)^#{2,4}\s+.*?(?:Exercise|Problem)\s*\d', text)
        if not exercise_headings:
            exercise_section = re.split(r'(?im)^## Exercises\s*$', text)[-1]
            prompts = exercise_section.split('<details', 1)[0]
            exercise_headings = re.findall(r'(?m)^[1-6]\.\s+\S', prompts)
        if len(exercise_headings) < 6:
            errors.append(f'{source.name}: expected six numbered worked exercises')
        solutions = [panel for panel in details if 'lab' not in panel.get('class', [])]
        solution_count = len(solutions)
        if len(solutions) == 1:
            solution_count = len(solutions[0].select(':scope > ol > li'))
        if solution_count != 6:
            errors.append(f'{source.name}: expected six expandable worked solutions, found {solution_count}')
        for url in re.findall(r'https://www\.youtube\.com/watch\?[^\s)"<>]+', text):
            split = urlsplit(url)
            from urllib.parse import parse_qs
            query = parse_qs(split.query)
            record = recordings.get(query.get('v', [''])[0])
            if not record:
                errors.append(f'{source.name}: unknown recording {url}')
                continue
            if record['lecture'] not in chapter['lectures']:
                # Related recordings may be cross-references; only out-of-bounds times fail.
                pass
            if 't' in query:
                token = query['t'][0]
                if not re.fullmatch(r'\d+(?:\.\d+)?s?', token):
                    errors.append(f'{source.name}: unsupported timestamp {token}')
                elif float(token.rstrip('s')) > record['duration_seconds']:
                    errors.append(f'{source.name}: timestamp beyond source duration')
        environment = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
                           MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
        print(f'Checking {meta.stem}; running {lab.name}', flush=True)
        if shared_process:
            # Each run gets separate globals. Scientific-library imports are
            # shared to avoid repeated native startup on constrained machines.
            output, diagnostics, code = io.StringIO(), io.StringIO(), 0
            try:
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(diagnostics):
                    runpy.run_path(str(lab), run_name='__main__')
            except Exception:
                import traceback
                diagnostics.write(traceback.format_exc())
                code = 1
            result = subprocess.CompletedProcess([str(lab)], code,
                                                  output.getvalue(), diagnostics.getvalue())
        else:
            try:
                result = subprocess.run([sys.executable, str(lab)], cwd=ROOT,
                                        capture_output=True, text=True, encoding='utf-8',
                                        timeout=180, env=environment)
            except subprocess.TimeoutExpired:
                errors.append(f'{lab.name}: execution exceeded 180 seconds')
                result = subprocess.CompletedProcess([str(lab)], 124, '', 'Execution timeout')
        labs.append(dict(file=lab.relative_to(ROOT).as_posix(), sha256=sha(lab),
                         exit_code=result.returncode, stdout=result.stdout.strip(),
                         stderr=result.stderr.strip()))
        if result.returncode:
            errors.append(f'{lab.name}: execution failed')
        chapters.append(dict(chapter=number, source_sha256=sha(source),
                             html_sha256=sha(page), words=len(re.findall(r'\b[\w-]+\b', text)),
                             exercises=len(exercise_headings), solution_panels=len(solutions),
                             worked_solutions=solution_count))
    if not allow_partial and sorted(covered) != list(range(1, 41)):
        errors.append('Chapter map does not cover every lecture exactly once')
    elif any(v > 1 for v in Counter(covered).values()):
        errors.append('Duplicate chapter coverage')
    for page in sorted(ROOT.glob('*.html')):
        soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        if not soup.title or not soup.html or soup.html.get('lang') != 'en':
            errors.append(f'{page.name}: missing title or language')
        if len(soup.select('h1')) != 1:
            errors.append(f'{page.name}: expected one H1')
        ids = [node['id'] for node in soup.select('[id]')]
        if len(ids) != len(set(ids)):
            errors.append(f'{page.name}: duplicate HTML identifiers')
        for node in soup.select('[href], [src]'):
            url = node.get('href', node.get('src', ''))
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                if parts.scheme not in ('https', 'mailto', 'data'):
                    errors.append(f'{page.name}: unsafe or local URL scheme')
                continue
            target = (page.parent / unquote(parts.path)).resolve() if parts.path else page
            if not target.is_relative_to(ROOT):
                errors.append(f'{page.name}: link leaves package')
                continue
            if not target.exists():
                errors.append(f'{page.name}: missing link {url}')
                continue
            if parts.fragment and target.suffix == '.html':
                destination = soup if target == page else BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
                if not destination.find(id=unquote(parts.fragment)):
                    errors.append(f'{page.name}: missing anchor {url}')
            link_count += 1
        if any(node.get('src', '').startswith('https:') for node in soup.select('script, img')):
            errors.append(f'{page.name}: external rendering dependency')
    report = dict(status='pass' if not errors else 'fail', chapter_count=len(chapters),
                  execution_mode='separate globals, shared interpreter' if shared_process else 'fresh process per lab',
                  covered_lectures=sorted(covered), chapters=chapters, labs=labs,
                  local_links_checked=link_count, errors=errors,
                  versions={name: importlib.metadata.version(name)
                            for name in ['Markdown', 'beautifulsoup4', 'numpy', 'scipy']},
                  scope='Mechanical/code validation; separate scientific review required.')
    (ROOT / 'validation' / 'package-checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=report['status'], chapters=len(chapters), labs=len(labs),
                          local_links=link_count, errors=errors), indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-partial', action='store_true')
    parser.add_argument('--shared-process', action='store_true',
                        help='Reuse imports while keeping each lab in separate globals')
    args = parser.parse_args()
    sys.exit(check(args.allow_partial, args.shared_process))
