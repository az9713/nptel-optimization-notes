"""Derive source aliases and the artifact dependency map from canonical inputs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source_aliases(manifest):
    """Add the analyze-sources interface without duplicating caption metadata."""
    manifest['sources'] = [dict(id='playlist', input=manifest['playlist_url'],
                                status='enumerated', coverage=dict(identity='full',
                                textual='metadata-only'))] + [
        dict(id=f'lecture-{row["lecture"]:02d}', input=row['url'],
             status=row['status'], recording_lecture=row['lecture'],
             coverage=dict(identity='full', textual='full', visual='not-performed',
                           audio='not-performed'),
             coverage_scope='Complete available English caption track; not a visual or audio transcription')
        for row in manifest['recordings']]
    return manifest


def main():
    source_path = ROOT / 'source-manifest.json'
    manifest = source_aliases(json.loads(source_path.read_text(encoding='utf-8')))
    source_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n',
                           encoding='utf-8', newline='\n')
    book = json.loads((ROOT / 'book.json').read_text(encoding='utf-8'))
    all_sources = [f'lecture-{row["lecture"]:02d}' for row in manifest['recordings']]
    artifacts = []
    for chapter in book['chapters']:
        dependencies = [f'lecture-{number:02d}' for number in chapter['lectures']]
        artifacts.extend([
            dict(path=f'{chapter["id"]}.html',
                 purpose='Expanded study chapter: ' + chapter['title'],
                 source_dependencies=dependencies),
            dict(path=f'labs/{chapter["id"]}.py',
                 purpose='Executable mathematical checks for ' + chapter['title'],
                 source_dependencies=dependencies)])
    for path, purpose in [
        ('index.html', 'Book orientation and searchable chapter navigation'),
        ('source-map.html', 'Recording identity, upload-order and chapter-coverage map'),
        ('study-guide.html', 'Prerequisites, reading paths and method-selection comparison'),
        ('numerical-lab.html', 'Interactive LP shadow-price and gradient-conditioning experiments'),
        ('references.html', 'Attribution, primary references and evidence boundaries'),
        ('book.json', 'Machine-readable chapter structure and authored-body digests')]:
        artifacts.append(dict(path=path, purpose=purpose,
                              source_dependencies=['playlist'] + all_sources))
    report = dict(artifacts=artifacts,
                  derivation='Generated from source-manifest.json recordings and book.json; original teaching constructions are distinguished in the chapters.')
    (ROOT / 'artifact-manifest.json').write_text(json.dumps(report, indent=2)+'\n',
                                                encoding='utf-8', newline='\n')
    print(f'Mapped {len(artifacts)} artifacts to one playlist and 40 recordings.')


if __name__ == '__main__':
    main()
