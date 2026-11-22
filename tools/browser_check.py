"""Exercise offline reader, MathJax and responsive equation scrolling."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from check_math_layout import MEASURE_LAYOUT

ROOT = Path(__file__).resolve().parents[1]


def run(browser_path=None, base_url=None, screenshot=False):
    results, errors = [], []
    files = sorted(ROOT.glob('ch[0-9][0-9].html'))
    support = [ROOT / name for name in ['index.html', 'source-map.html', 'study-guide.html', 'numerical-lab.html', 'references.html']]
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=browser_path,
                                     ignore_default_args=['--hide-scrollbars'])
        for width, height in [(1440, 1000), (390, 844)]:
            context = browser.new_context(viewport=dict(width=width, height=height))
            if not base_url:
                context.route('https://**/*', lambda route: route.abort())
                context.route('http://**/*', lambda route: route.abort())
            page = context.new_page()
            page_errors = []
            page.on('pageerror', lambda exc: page_errors.append(str(exc)))
            for file in support + files:
                target = f'{base_url.rstrip("/")}/{file.name}' if base_url else file.as_uri()
                before = len(page_errors)
                response = page.goto(target, wait_until='load')
                if response and not response.ok:
                    errors.append(f'{file.name}/{width}: HTTP {response.status}')
                page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise')
                page.evaluate('() => MathJax.startup.promise.then(() => undefined)')
                layout = page.evaluate(MEASURE_LAYOUT)
                if width < 721:
                    page.locator('#menu').click()
                    if page.locator('#menu').get_attribute('aria-expanded') != 'true':
                        errors.append(f'{file.name}/{width}: contents toggle failed')
                    page.locator('#menu').click()
                if file in files:
                    page.locator('#solutions').click()
                    if not page.locator('article details').evaluate_all('(nodes) => nodes.every(n => n.open)'):
                        errors.append(f'{file.name}/{width}: solution toggle failed')
                    # Hidden solution equations need a second layout measurement after expansion.
                    layout = page.evaluate(MEASURE_LAYOUT)
                    if layout['rendered'] == 0:
                        errors.append(f'{file.name}/{width}: no mathematics rendered')
                    page.locator('#solutions').click()
                if file.name == 'index.html':
                    expected = sum('duality' in text.lower() for text in page.locator('.chapter-card').all_inner_texts())
                    page.locator('#search').fill('duality')
                    count = page.locator('.chapter-card:visible').count()
                    if count != expected:
                        errors.append(f'index/{width}: chapter filter expected {expected} duality matches, got {count}')
                    page.locator('#search').fill('unfindableterm')
                    if page.locator('.chapter-card:visible').count() != 0:
                        errors.append(f'index/{width}: empty-result filter failed')
                    page.locator('#search').fill('')
                if file.name == 'numerical-lab.html':
                    page.locator('#capacity').fill('2')
                    page.locator('#capacity').dispatch_event('input')
                    if '[2, 3]' not in page.locator('#lp-price').inner_text():
                        errors.append(f'lab/{width}: shadow-price breakpoint mismatch')
                    page.locator('#conditioning').fill('1')
                    page.locator('#conditioning').dispatch_event('input')
                    if '0.0000e+0' not in page.locator('#gradient-result').inner_text():
                        errors.append(f'lab/{width}: identity quadratic must converge in one step')
                for key in ['mathErrors', 'unhiddenInlineScrollers', 'blockedOverflow', 'pageOverflow']:
                    if layout[key]:
                        errors.append(f'{file.name}/{width}: {key}={layout[key]}')
                if layout['pageOverflow']:
                    layout['overflowing_elements'] = page.evaluate('''() =>
                        [...document.querySelectorAll('p,h1,h2,h3,pre,li,table,a,details,mjx-container')]
                        .map(e => ({tag: e.tagName, cls: e.className,
                            right: e.getBoundingClientRect().right,
                            text: e.textContent.slice(0, 100)}))
                        .filter(e => e.right > innerWidth + 1).slice(0, 20)''')
                if len(page_errors) > before:
                    errors.extend(f'{file.name}/{width}: {e}' for e in page_errors[before:])
                results.append(dict(file=file.name, width=width, **layout))
                print(f'{file.name} {width}: {layout}', flush=True)
                if screenshot and width == 1440 and file.name in ('ch01.html', 'index.html', 'numerical-lab.html'):
                    (ROOT / 'work').mkdir(exist_ok=True)
                    page.screenshot(path=str(ROOT / 'work' / f'{file.stem}-desktop.png'))
                if screenshot and width == 390 and file.name == 'ch01.html':
                    page.screenshot(path=str(ROOT / 'work' / 'ch01-mobile.png'))
            context.close()
        browser.close()
    report = dict(status='pass' if not errors else 'fail', pages=results, errors=errors,
                  offline=not bool(base_url), browser='Chromium',
                  scope='Desktop/mobile DOM, equations, controls, filtering and interactive models.')
    name = 'live-browser-checks.json' if base_url else 'browser-checks.json'
    (ROOT / 'validation' / name).write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=report['status'], checks=len(results), errors=errors), indent=2))
    return bool(errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser')
    parser.add_argument('--base-url')
    parser.add_argument('--screenshots', action='store_true')
    args = parser.parse_args()
    raise SystemExit(run(args.browser, args.base_url, args.screenshots))
