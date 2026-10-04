"""Download a single public Douyin video through its mobile browser page."""
import argparse
import asyncio
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright


def input_target(text):
    text = text.strip().replace('\\&', '&').replace('\\_', '_').replace('&amp;', '&')
    if re.fullmatch(r'\d{15,25}', text):
        return text, None
    match = re.search(r'https?://[^\s<>"，。]+', text)
    if not match:
        raise ValueError('Input must contain a Douyin URL or video ID')
    url = match.group().rstrip(')）]')
    host = urllib.parse.urlsplit(url).hostname or ''
    if not (host == 'douyin.com' or host.endswith('.douyin.com') or host == 'iesdouyin.com' or host.endswith('.iesdouyin.com')):
        raise ValueError('Only Douyin links are supported')
    return extract_id(url), url


def extract_id(url):
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
    for key in ('modal_id', 'aweme_id', 'item_ids'):
        value = query.get(key, [''])[0]
        if re.fullmatch(r'\d{15,25}', value):
            return value
    match = re.search(r'/(?:video|note|slides)/(\d{15,25})(?:/|$|\?)', url)
    return match.group(1) if match else None


def find_item(data, video_id):
    if isinstance(data, dict):
        if str(data.get('aweme_id', '')) == video_id and ('video' in data or 'images' in data):
            return data
        for value in data.values():
            found = find_item(value, video_id)
            if found:
                return found
    elif isinstance(data, list):
        for value in data:
            found = find_item(value, video_id)
            if found:
                return found
    return None


def parse_html(html, video_id):
    decoder = json.JSONDecoder()
    for match in re.finditer(r'(?:window\.)?_ROUTER_DATA\s*=\s*', html):
        try:
            data, _ = decoder.raw_decode(html[match.end():])
            if isinstance(data, str):
                data = json.loads(data)
            item = find_item(data, video_id)
            if item:
                return item
        except (ValueError, TypeError):
            continue
    return None


def media_urls(item):
    if item.get('images'):
        raise ValueError('This item is an image gallery, not a single video')
    video = item.get('video') or {}
    urls = []
    for key in ('play_addr', 'play_addr_h264', 'download_addr'):
        for url in (video.get(key) or {}).get('url_list', []):
            if isinstance(url, str) and url.startswith(('https://', 'http://')) and url not in urls:
                urls.append(url)
    if not urls:
        raise ValueError('Matching video has no downloadable media URL')
    return urls[:3]


def browser_error_message(exc):
    """Return a useful, credential-safe explanation for browser failures."""
    message = str(exc)
    lowered = message.lower()
    if 'captcha' in lowered or '验证码' in message:
        return 'CAPTCHA required; stop and use an authorized interactive browser session'
    if 'err_ssl_protocol_error' in lowered or 'wrong version number' in lowered:
        return 'Network TLS handshake failed while contacting Douyin; check outbound HTTPS connectivity and proxy configuration'
    if 'err_name_not_resolved' in lowered or 'name or service not known' in lowered:
        return 'Network DNS lookup failed while contacting Douyin; check DNS and outbound network access'
    if any(token in lowered for token in ('err_connection_reset', 'err_connection_refused', 'err_connection_closed', 'internet_disconnected')):
        return 'Network connection failed while contacting Douyin; check outbound network access and proxy configuration'
    if 'timeout' in lowered or 'timed out' in lowered:
        return 'Timed out while contacting Douyin; check network access or retry later'
    if 'error while loading shared libraries' in lowered or 'cannot open shared object file' in lowered:
        return 'Chromium system dependency is missing; install Playwright Chromium dependencies'
    return f'Browser navigation failed ({type(exc).__name__})'


def public_error_message(exc):
    """Keep expected diagnostics while never returning raw browser/network logs."""
    message = str(exc)
    safe_markers = (
        'CAPTCHA required',
        'Network TLS handshake failed',
        'Network DNS lookup failed',
        'Network connection failed',
        'Timed out while contacting Douyin',
        'No matching video data returned by mobile page',
        'This item is an image gallery, not a single video',
        'Matching video has no downloadable media URL',
        'No valid video stream or duration',
        'ffprobe could not read the downloaded video',
        'Full video decode failed',
        'Media download/validation failed:',
        'Missing dependency:',
        'A previous .part file exists',
        'Destination appeared during download',
    )
    if any(marker in message for marker in safe_markers):
        return message
    return browser_error_message(exc)


def verify(path):
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], capture_output=True, text=True, timeout=60)
    if probe.returncode:
        raise ValueError('ffprobe could not read the downloaded video')
    data = json.loads(probe.stdout)
    videos = [s for s in data.get('streams', []) if s.get('codec_type') == 'video']
    if not videos or float(data.get('format', {}).get('duration', 0)) <= 0:
        raise ValueError('No valid video stream or duration')
    decode = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'], capture_output=True, timeout=180)
    if decode.returncode:
        raise ValueError('Full video decode failed')
    return {'duration': float(data['format']['duration']), 'width': videos[0]['width'], 'height': videos[0]['height'], 'bytes': path.stat().st_size, 'has_audio': any(s.get('codec_type') == 'audio' for s in data['streams']), 'verified': True}


def save_media(urls, user_agent, destination):
    part = destination.with_suffix('.mp4.part')
    if part.exists():
        raise FileExistsError('A previous .part file exists; choose another output directory or inspect it first')
    errors = []
    for url in urls:
        try:
            request = urllib.request.Request(url, headers={'User-Agent': user_agent, 'Referer': 'https://www.douyin.com/'})
            started = time.monotonic()
            with urllib.request.urlopen(request, timeout=30) as response, part.open('wb') as output:
                if response.status != 200:
                    raise ValueError('Media server did not return a complete HTTP 200 response')
                expected = int(response.headers.get('Content-Length', '0'))
                total = 0
                while chunk := response.read(1024 * 1024):
                    total += len(chunk)
                    if total > 1024 ** 3 or time.monotonic() - started > 180:
                        raise ValueError('Download exceeded 1 GiB or 180 seconds')
                    output.write(chunk)
                if expected and total != expected:
                    raise ValueError('Downloaded size differs from Content-Length')
            details = verify(part)
            # rename is non-overwriting on Windows; check again for ordinary use elsewhere.
            if destination.exists():
                raise FileExistsError('Destination appeared during download')
            part.rename(destination)
            return details
        except Exception as exc:
            errors.append(type(exc).__name__)
    raise RuntimeError('Media download/validation failed: ' + ', '.join(errors))


async def run(args):
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            raise RuntimeError(f'Missing dependency: {tool}')
    video_id, source = input_target(args.input)
    directory = Path(args.output_dir).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        options = {'headless': True}
        if args.channel:
            options['channel'] = args.channel
        browser = await p.chromium.launch(**options)
        try:
            context = await browser.new_context(**p.devices['iPhone 13'])
            page = await context.new_page()
            if not video_id:
                await page.goto(source, wait_until='domcontentloaded', timeout=30000)
                video_id = extract_id(page.url)
                if not video_id:
                    raise ValueError('Could not resolve video ID from short link')
            destination = directory / f'{video_id}.mp4'
            if destination.exists():
                return {'success': True, 'video_id': video_id, 'path': str(destination), 'reused': True, **await asyncio.to_thread(verify, destination)}
            item = None
            errors = []
            for url in (f'https://www.douyin.com/video/{video_id}', f'https://m.douyin.com/share/video/{video_id}'):
                try:
                    await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                    for _ in range(15):
                        if '验证码' in await page.title():
                            raise RuntimeError('CAPTCHA required')
                        item = parse_html(await page.content(), video_id)
                        if item:
                            break
                        await page.wait_for_timeout(2000)
                    if item:
                        break
                    errors.append('No matching video data returned by mobile page')
                except Exception as exc:
                    errors.append(browser_error_message(exc))
            if not item:
                raise RuntimeError('; '.join(errors))
            details = await asyncio.to_thread(save_media, media_urls(item), await page.evaluate('navigator.userAgent'), destination)
            result = {'success': True, 'video_id': video_id, 'title': item.get('desc', ''), 'author': (item.get('author') or {}).get('nickname', ''), 'path': str(destination), **details}
            metadata = destination.with_suffix('.json')
            if not metadata.exists():
                with metadata.open('x', encoding='utf-8') as file:
                    json.dump(result, file, ensure_ascii=False, indent=2)
            return result
        finally:
            await browser.close()


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Douyin URL, share text or video ID')
    parser.add_argument('--output-dir', default='downloads')
    parser.add_argument('--channel', choices=['msedge', 'chrome'], help='Use installed browser instead of bundled Chromium')
    args = parser.parse_args()
    try:
        result = asyncio.run(run(args))
    except Exception as exc:
        # Browser exceptions can include signed media URLs, cookies, and full logs.
        message = public_error_message(exc)
        print(json.dumps({'success': False, 'error': message}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
