"""Acquire compact English captions, never video; keep raw text local."""
import concurrent.futures
import hashlib
import gzip
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from manifest_artifacts import source_aliases

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work'


def acquire(pair):
    position, entry = pair
    number = int(re.search(r'Lec-(\d+)', entry['title']).group(1))
    video_id = entry['id']
    target = WORK / 'transcripts' / f'{number:02d}.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    record = dict(lecture=number, playlist_position=position,
                  video_id=video_id, title=entry['title'],
                  duration_seconds=entry.get('duration'),
                  url=f'https://www.youtube.com/watch?v={video_id}')
    for attempt in range(3):
        try:
            if target.with_suffix('.json.gz').exists():
                payload = json.loads(gzip.decompress(target.with_suffix('.json.gz').read_bytes()))
                target.write_bytes(gzip.decompress(target.with_suffix('.json.gz').read_bytes()))
            elif target.exists():
                payload = json.loads(target.read_text(encoding='utf-8'))
            else:
                tracks = YouTubeTranscriptApi().list(video_id)
                try:
                    track = tracks.find_manually_created_transcript(['en'])
                except Exception:
                    track = tracks.find_generated_transcript(['en'])
                fetched = track.fetch()
                payload = dict(language=track.language_code,
                               is_generated=track.is_generated,
                               retrieved_at=datetime.now(timezone.utc).isoformat(),
                               segments=fetched.to_raw_data())
                target.write_text(json.dumps(payload, ensure_ascii=False,
                                             separators=(',', ':')), encoding='utf-8')
            segments = payload['segments']
            text = '\n'.join(f"[{s['start']:.2f}] {s['text']}" for s in segments)
            (target.with_suffix('.txt')).write_text(text, encoding='utf-8')
            end = max(s['start'] + s['duration'] for s in segments)
            record.update(status='acquired', language=payload['language'],
                          is_generated=payload['is_generated'],
                          retrieved_at=payload['retrieved_at'],
                          transcript_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                          segment_count=len(segments), last_caption_end=round(end, 3),
                          first_caption_start=segments[0]['start'])
            print(f'{number:02d}: acquired {len(segments)} segments', flush=True)
            return record
        except Exception as exc:
            error = f'{type(exc).__name__}: {str(exc)[:300]}'
            time.sleep(1 + attempt)
    record.update(status='blocked', error=error)
    print(f'{number:02d}: BLOCKED {error}', flush=True)
    return record


if __name__ == '__main__':
    if (WORK / 'playlist.json').exists():
        playlist = json.loads((WORK / 'playlist.json').read_text(encoding='utf-8-sig'))
    else:
        prior = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
        playlist = dict(title=prior['title'], webpage_url=prior['playlist_url'], entries=[
            dict(id=r['video_id'], title=r['title'], duration=r['duration_seconds'])
            for r in sorted(prior['recordings'], key=lambda r: r['playlist_position'])])
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(acquire, enumerate(playlist['entries'], 1)))
    manifest = dict(title=playlist['title'], playlist_url=playlist['webpage_url'],
                    inventory_retrieved_at=datetime.now(timezone.utc).isoformat(),
                    coverage=dict(identity='full', textual='full' if all(
                        r['status'] == 'acquired' for r in rows) else 'partial',
                        visual='not-performed', audio='not-performed'),
                    recordings=sorted(rows, key=lambda r: r['lecture']))
    (ROOT / 'source-manifest.json').write_text(json.dumps(source_aliases(manifest), indent=2)+'\n',
                                              encoding='utf-8', newline='\n')
