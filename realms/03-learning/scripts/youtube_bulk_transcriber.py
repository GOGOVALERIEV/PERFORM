"""
YouTube Bulk Transcriber
========================
Transcribes YouTube channels/videos without getting rate-limited.

HOW IT WORKS:
Uses yt-dlp's android VR player client to fetch subtitles. YouTube has a separate
API endpoint for VR devices (like Meta Quest) that doesn't have the same rate limits
as the normal web timedtext API. Same subtitle data, different door, no blocks.

USAGE:
    # Transcribe a single video
    python tools/youtube_bulk_transcriber.py --video VIDEO_ID

    # Transcribe a whole channel (last 5 months, skips Shorts)
    python tools/youtube_bulk_transcriber.py --channel https://www.youtube.com/@ChannelName

    # Transcribe multiple channels from a JSON config
    python tools/youtube_bulk_transcriber.py --config channels.json

    # Change output folder and months
    python tools/youtube_bulk_transcriber.py --channel URL --output ./my_transcripts --months 3

CONFIG FILE FORMAT (channels.json):
    [
        {"url": "https://www.youtube.com/@ChannelName", "name": "Channel Name"},
        {"url": "https://www.youtube.com/@Other", "name": "Other Channel"}
    ]

OUTPUT:
    output_folder/
        Channel Name/
            20260101_Video Title.txt
            20260102_Another Video.txt
        Other Channel/
            ...

REQUIREMENTS:
    pip install yt-dlp
"""

import os, re, json, time, random, sys, io, tempfile, shutil, argparse
from datetime import datetime, timedelta
from pathlib import Path
import yt_dlp

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def get_channel_videos(channel_url, months_back=5, max_videos=80):
    cutoff = datetime.now() - timedelta(days=months_back * 30)
    opts = {'extract_flat': 'in_playlist', 'quiet': True, 'no_warnings': True, 'playlistend': max_videos}
    videos = []
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f'{channel_url}/videos', download=False)
        if not info or 'entries' not in info:
            return []
        for e in info['entries']:
            if e is None:
                continue
            dur = e.get('duration') or 0
            try:
                dur = int(float(dur))
            except:
                dur = 0
            if dur <= 60:
                continue
            date = e.get('upload_date', '')
            if date:
                try:
                    if datetime.strptime(date, '%Y%m%d') < cutoff:
                        continue
                except:
                    pass
            videos.append({'id': e.get('id', ''), 'title': e.get('title', 'Unknown'), 'date': date or 'unknown', 'duration': dur})
    return videos


def safe_filename(title):
    s = re.sub(r'[<>:"/\\|?*]', '', title)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:100] if len(s) > 100 else s


def get_transcript(video_id):
    tmpdir = tempfile.mkdtemp()
    outpath = os.path.join(tmpdir, 'sub')
    ydl_opts = {
        'writeautomaticsub': True, 'writesubtitles': True,
        'subtitleslangs': ['en'], 'subtitlesformat': 'json3',
        'skip_download': True, 'quiet': True, 'no_warnings': True,
        'outtmpl': outpath,
        'extractor_args': {'youtube': {'player_client': ['android_vr']}},
        'ignore_no_formats_error': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
        for f in os.listdir(tmpdir):
            if f.endswith('.json3'):
                with open(os.path.join(tmpdir, f), 'r', encoding='utf-8') as fh:
                    data = json.loads(fh.read())
                texts = []
                for ev in data.get('events', []):
                    for seg in ev.get('segs', []):
                        t = seg.get('utf8', '').strip()
                        if t and t != '\n':
                            texts.append(t)
                shutil.rmtree(tmpdir, ignore_errors=True)
                return ' '.join(texts) if texts else None
    except:
        pass
    shutil.rmtree(tmpdir, ignore_errors=True)
    return None


def transcribe_channel(channel_url, channel_name, output_base, months_back=5, delay=3):
    print(f'\n{"="*60}')
    print(f'  {channel_name}')
    print(f'{"="*60}')

    ch_dir = Path(output_base) / channel_name
    ch_dir.mkdir(parents=True, exist_ok=True)

    videos = get_channel_videos(channel_url, months_back)
    print(f'  Found {len(videos)} videos (last {months_back} months, no Shorts)')

    done, skipped, failed = 0, 0, 0
    for i, v in enumerate(videos):
        fn = f'{v["date"]}_{safe_filename(v["title"])}.txt'
        fp = ch_dir / fn

        if fp.exists() and fp.stat().st_size > 100:
            skipped += 1
            continue

        print(f'  [{i+1}/{len(videos)}] {v["title"][:55]}', flush=True)
        text = get_transcript(v['id'])
        if text and len(text) > 50:
            header = f'Title: {v["title"]}\nChannel: {channel_name}\nDate: {v["date"]}\nDuration: {v["duration"]//60} minutes\nURL: https://www.youtube.com/watch?v={v["id"]}\n' + '-' * 60 + '\n\n'
            fp.write_text(header + text, encoding='utf-8')
            print(f'           DONE - {len(text):,} chars', flush=True)
            done += 1
        else:
            print(f'           FAIL - no subs', flush=True)
            failed += 1
        time.sleep(delay + random.uniform(0.5, 1.5))

    print(f'  --- {channel_name}: {done} done | {skipped} skipped | {failed} failed ---')
    return done, skipped, failed


def main():
    parser = argparse.ArgumentParser(description='YouTube Bulk Transcriber (android_vr bypass)')
    parser.add_argument('--video', help='Single video ID to transcribe')
    parser.add_argument('--channel', help='Channel URL to transcribe')
    parser.add_argument('--config', help='JSON config file with channel list')
    parser.add_argument('--output', default='./transcripts', help='Output folder (default: ./transcripts)')
    parser.add_argument('--months', type=int, default=5, help='How many months back (default: 5)')
    parser.add_argument('--delay', type=int, default=3, help='Seconds between requests (default: 3)')
    args = parser.parse_args()

    if args.video:
        print(f'Transcribing video: {args.video}')
        text = get_transcript(args.video)
        if text:
            out = Path(args.output)
            out.mkdir(parents=True, exist_ok=True)
            fp = out / f'{args.video}.txt'
            fp.write_text(text, encoding='utf-8')
            print(f'DONE - {len(text):,} chars saved to {fp}')
        else:
            print('FAILED - no subtitles found')

    elif args.channel:
        name = args.channel.split('/')[-1].replace('@', '')
        transcribe_channel(args.channel, name, args.output, args.months, args.delay)

    elif args.config:
        with open(args.config, 'r') as f:
            channels = json.loads(f.read())
        gt, gs, gf = 0, 0, 0
        for ch in channels:
            d, s, f_ = transcribe_channel(ch['url'], ch['name'], args.output, args.months, args.delay)
            gt += d; gs += s; gf += f_
            time.sleep(10)
        print(f'\n{"="*60}')
        print(f'  ALL DONE: {gt} transcribed | {gs} skipped | {gf} failed')
        print(f'{"="*60}')

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
