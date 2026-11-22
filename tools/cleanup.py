"""Compress and verify local transcripts, then remove generated temporary work."""
import gzip
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = (ROOT / 'work').resolve()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if WORK.parent != ROOT or WORK.name != 'work':
        raise RuntimeError('Unexpected work directory; refusing cleanup')
    manifest = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
    retained = []
    for record in manifest['recordings']:
        stem = f'{record["lecture"]:02d}'
        raw = WORK / 'transcripts' / f'{stem}.json'
        compressed = raw.with_suffix('.json.gz')
        if raw.exists():
            data = raw.read_bytes()
            if sha(data) != record['transcript_sha256']:
                raise RuntimeError(f'{stem}: transcript digest mismatch; retain original')
            compressed.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
        if not compressed.exists() or sha(gzip.decompress(compressed.read_bytes())) != record['transcript_sha256']:
            raise RuntimeError(f'{stem}: retained archive did not verify')
        retained.append(dict(lecture=record['lecture'], file=compressed.name,
                             compressed_bytes=compressed.stat().st_size,
                             decompressed_sha256=record['transcript_sha256']))
    # Delete redundant representations only after all forty archives verify.
    for entry in (WORK / 'transcripts').iterdir():
        if entry.suffix in ('.txt', '.json') and entry.stem.isdigit():
            entry.unlink()
    removed = []
    for entry in WORK.iterdir():
        resolved = entry.resolve()
        if resolved.parent != WORK:
            raise RuntimeError('Unexpected cleanup target')
        if entry.name == 'transcripts':
            continue
        removed.append(entry.name)
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    # Python caches are reproducible and contain no source evidence.
    for entry in ROOT.rglob('__pycache__'):
        if entry.resolve().is_relative_to(ROOT) and '.git' not in entry.parts:
            shutil.rmtree(entry)
    media = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
             if p.is_file() and p.suffix.lower() in ('.mp4', '.webm', '.m4a', '.wav', '.mkv')]
    if media:
        raise RuntimeError(f'Unexpected media still present: {media}')
    report = dict(status='pass', retained_transcripts=retained,
                  raw_video_files_retained=len(media), removed_temporary_entries=removed,
                  notes='Raw caption JSON remains recoverable byte-for-byte from gzip. Temporary media and source captures are not retained.')
    (ROOT / 'validation' / 'cleanup.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f'Verified and retained {len(retained)} compact transcripts; removed {len(removed)} temporary entries.')


if __name__ == '__main__':
    main()
