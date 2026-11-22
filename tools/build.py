"""Build the offline reader deterministically from authored Markdown."""
import hashlib
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import markdown
# Inputs are already decoded UTF-8. Optional byte-encoding detectors are unused;
# do not load their native extensions just to parse Unicode strings.
sys.modules.setdefault('chardet', None)
sys.modules.setdefault('cchardet', None)
sys.modules.setdefault('charset_normalizer', None)
sys.modules.setdefault('lxml', None)
sys.modules.setdefault('html5lib', None)
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'Optimization: Models, Algorithms, and Decisions'
REPO = 'nptel-optimization-notes'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_markdown(source):
    """Shield TeX from Markdown and HTML interpretation; keep code literal."""
    source = re.sub(r'<details(?![^>]*\bmarkdown=)([^>]*)>',
                    r'<details markdown="1"\1>', source)
    stash = {}
    pieces = re.split(r'(```[^\n]*\n.*?```)', source, flags=re.S)
    pattern = re.compile(r'\$\$.*?\$\$|(?<![\\$])\$(?!\$)(?:\\.|[^$\\\n])*?(?<!\\)\$(?!\$)', re.S)
    for index in range(0, len(pieces), 2):
        def save(match):
            key = f'MATHPLACEHOLDER{len(stash):06d}END'
            stash[key] = html.escape(match.group(0), quote=False)
            return key
        pieces[index] = pattern.sub(save, pieces[index])
    result = markdown.markdown(''.join(pieces), extensions=['fenced_code', 'tables', 'toc', 'sane_lists', 'md_in_html'],
                               extension_configs={'toc': {'permalink': False}})
    for key, value in stash.items():
        result = result.replace(key, value)
    soup = BeautifulSoup(result, 'html.parser')
    for table in soup.select('table'):
        table.wrap(soup.new_tag('div', attrs={'class': 'tablewrap'}))
    for pre in soup.select('pre'):
        wrapper = soup.new_tag('div', attrs={'class': 'codewrap'})
        pre.wrap(wrapper)
        button = soup.new_tag('button', attrs={'class': 'copybtn', 'type': 'button',
                                              'aria-label': 'Copy code'})
        button.string = 'Copy'
        wrapper.insert(0, button)
    for anchor in soup.select('a[href]'):
        href = anchor['href']
        if href.startswith('../'):
            anchor['href'] = href[3:]
        if re.match(r'^(?:\.?/?chapters/)?ch\d\d\.md(?:#.*)?$', anchor['href']):
            anchor['href'] = re.sub(r'^(?:\.?/?chapters/)?', '', anchor['href']).replace('.md', '.html')
    # The metadata supplies the page's one H1; authors can include a source title.
    if soup.h1:
        soup.h1.decompose()
    return str(soup)


def load_chapters():
    rows = []
    for path in sorted((ROOT / 'chapters').glob('ch[0-9][0-9].json')):
        row = json.loads(path.read_text(encoding='utf-8-sig'))
        row['id'] = path.stem
        row['number'] = int(path.stem[2:])
        row['markdown'] = ROOT / 'chapters' / f'{path.stem}.md'
        if not row['markdown'].exists():
            continue
        row['body_sha256'] = digest(row['markdown'])
        row['words'] = len(re.findall(r'\b[\w-]+\b', row['markdown'].read_text(encoding='utf-8')))
        rows.append(row)
    return rows


def shell(title, content, chapters, current='', toc='', extra_script=''):
    nav = ''.join(f'<a href="{r["id"]}.html"'
                  f'{" aria-current=page" if current == r["id"] else ""}>'
                  f'{r["number"]:02d} · {html.escape(r["title"])}</a>' for r in chapters)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Independent NPTEL Optimization study edition: 40 lectures, derivations, solved problems and executable labs.">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'">
<title>{html.escape(title)} · NPTEL Optimization</title><link rel="stylesheet" href="assets/reader.css">
<script src="assets/math-config.js" defer></script><script src="assets/mathjax-tex-svg.js" defer></script>
<script src="assets/reader.js" defer></script>{extra_script}</head><body>
<a class="skip" href="#main">Skip to main content</a><div class="shell">
<aside><a class="brand" href="index.html">Optimization</a><p>Models, algorithms, decisions<br>Independent NPTEL study edition</p>
<button id="menu" aria-expanded="false" aria-controls="navigation">Contents</button>
<nav id="navigation" aria-label="Book"><a href="index.html">Overview and chapter finder</a>
<a href="source-map.html">40 recordings and source map</a><a href="study-guide.html">Study guide and method map</a>
<a href="numerical-lab.html">Interactive optimization lab</a><a href="references.html">References and evidence limits</a>{nav}</nav></aside>
<main id="main"><div class="eyebrow">NPTEL · IIT Kharagpur · Optimization</div>{content}</main></div></body></html>
'''


def write_page(filename, title, content, chapters, current='', **kwargs):
    (ROOT / filename).write_text(shell(title, content, chapters, current, **kwargs), encoding='utf-8', newline='\n')


def build():
    chapters = load_chapters()
    manifest = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
    recordings = {r['lecture']: r for r in manifest['recordings']}
    for index, row in enumerate(chapters):
        source = row['markdown'].read_text(encoding='utf-8')
        body = render_markdown(source)
        soup = BeautifulSoup(body, 'html.parser')
        headings = soup.select('h2[id]')
        toc = '<div class="toc"><strong>In this chapter</strong><ul>' + ''.join(
            f'<li><a href="#{h["id"]}">{html.escape(h.get_text(" ", strip=True))}</a></li>'
            for h in headings) + '</ul></div>'
        source_links = ', '.join(f'<a href="{recordings[n]["url"]}">Lecture {n}</a>' for n in row['lectures'])
        objectives = ''.join(f'<li>{html.escape(x)}</li>' for x in row.get('objectives', []))
        lab_path = ROOT / 'labs' / f'{row["id"]}.py'
        lab = ''
        if lab_path.exists():
            code = html.escape(lab_path.read_text(encoding='utf-8'))
            lab = f'<details class="lab"><summary>Executable chapter laboratory</summary><p><a href="labs/{row["id"]}.py">Download Python source</a>. Run in a fresh interpreter; see requirements.txt.</p><div class="codewrap"><button class="copybtn" type="button" aria-label="Copy lab source">Copy</button><pre><code class="language-python">{code}</code></pre></div></details>'
        previous = f'<a rel="prev" href="{chapters[index-1]["id"]}.html">← {html.escape(chapters[index-1]["title"])}</a>' if index else '<a href="index.html">← Overview</a>'
        following = f'<a rel="next" href="{chapters[index+1]["id"]}.html">{html.escape(chapters[index+1]["title"])} →</a>' if index+1 < len(chapters) else '<a href="study-guide.html">Study guide →</a>'
        content = f'''<h1>{row["number"]:02d}. {html.escape(row["title"])}</h1>
<p class="meta">{source_links} · Original expanded exposition · {row["words"]:,} source words</p>
<div class="objectives"><strong>What you will learn</strong><ul>{objectives}</ul>
<p><strong>Prerequisites:</strong> {html.escape(row.get('prerequisites',''))}</p></div>
<div class="toolbar"><button id="solutions" type="button">Open solutions and code</button><button id="print" type="button">Print / save PDF</button>
<a href="chapters/{row["id"]}.md">Editable chapter source</a></div>{toc}
<article>{body}{lab}</article><div class="footer">{previous}{following}</div>'''
        write_page(f'{row["id"]}.html', row['title'], content, chapters, row['id'])
    cards = ''.join(f'<div class="chapter-card"><small>CHAPTER {r["number"]:02d} · LECTURES {", ".join(map(str,r["lectures"]))}</small><a href="{r["id"]}.html">{html.escape(r["title"])}</a><p>{html.escape(" · ".join(r.get("objectives",[])))}</p></div>' for r in chapters)
    overview = render_markdown((ROOT / 'overview.md').read_text(encoding='utf-8'))
    write_page('index.html', TITLE, f'<h1>{TITLE}</h1>{overview}<label for="search">Find a chapter by method or topic</label><input id="search" type="search" placeholder="Try duality, KKT, dynamic programming…"><p class="status" id="search-status" aria-live="polite">{len(chapters)} chapters shown</p><div class="chapter-list">{cards}</div>', chapters)
    rows = []
    for number, record in recordings.items():
        chapter = next((c for c in chapters if number in c['lectures']), None)
        chapter_link = f'<a href="{chapter["id"]}.html">{chapter["number"]:02d}</a>' if chapter else 'Pending'
        rows.append(f'<tr><td>{number}</td><td>{record["playlist_position"]}</td><td><a href="{record["url"]}">{html.escape(record["title"])}</a></td><td>{record["duration_seconds"]//60}:{record["duration_seconds"]%60:02d}</td><td>{chapter_link}</td></tr>')
    intro = '<h1>Recording and source map</h1><p>The playlist contains 40 recordings. This edition follows official lecture numbers. Playlist position 35 contains lecture 40; the next five entries contain lectures 35–39. Both orders remain visible below.</p><p>All English tracks were acquired as non-automatic captions. Source timing and topic coverage are available; slides, board notation and audio were not comprehensively audited. <a href="source-manifest.json">Machine-readable provenance</a>.</p>'
    write_page('source-map.html', 'Recording and source map', intro+'<div class="tablewrap"><table><thead><tr><th>Lecture</th><th>Playlist position</th><th>Original upload title</th><th>Duration</th><th>Chapter</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>', chapters)
    for stem, title in [('study-guide','Study guide and method map'), ('references','References and evidence limits'), ('numerical-lab','Interactive optimization laboratory')]:
        source_path = ROOT / f'{stem}.md'
        if source_path.exists():
            content = render_markdown(source_path.read_text(encoding='utf-8'))
            script = '<script src="assets/lab.js" defer></script>' if stem == 'numerical-lab' else ''
            write_page(f'{stem}.html', title, f'<h1>{title}</h1>{content}', chapters, extra_script=script)
    compact = [{k:v for k,v in c.items() if k != 'markdown'} for c in chapters]
    (ROOT / 'book.json').write_text(json.dumps(dict(title=TITLE, chapters=compact), indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
    print(f'Built {len(chapters)} chapters and 5 supporting pages.')


if __name__ == '__main__':
    build()
