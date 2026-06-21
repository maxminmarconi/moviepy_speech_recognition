import sys
import os
import yt_dlp
import subprocess


def need_convert_to_mp3(filepath):
    """
    判断是否需要转 MP3
    """

    ext = os.path.splitext(filepath)[1].lower()

    # 已经是 mp3，不需要转
    if ext == '.mp3':
        return False

    # m4a 默认也不转（你可以改成 True）
    if ext == '.m4a':
        return False

    # 其他全部转
    return True


def convert_to_mp3(input_file):
    """
    ffmpeg 转 mp3（带进度）
    """

    output_file = os.path.splitext(input_file)[0] + ".mp3"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-vn",
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        output_file
    ]

    print(f"\n开始转码: {input_file} → {output_file}")

    subprocess.run(cmd)

    print("转码完成")


def download_audio(url, cookies_path=None, fmt='bestaudio'):
    """
    下载音频 + 判断是否转码
    """

    os.makedirs("audios", exist_ok=True)

    downloaded_file = {"path": None}

    def hook(d):
        if d['status'] == 'finished':
            downloaded_file['path'] = d['filename']
            print(f"\n下载完成: {d['filename']}")

    ydl_opts = {
        'format': fmt,
        'outtmpl': 'audios/%(title)s.%(ext)s',

        'progress_hooks': [progress_hook, hook],

        'user_agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),

        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept-Language': 'en-US,en;q=0.9'
        }
    }

    if cookies_path and os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # =========================
    # ⭐ 核心判断逻辑
    # =========================
    file_path = downloaded_file['path']

    if file_path and need_convert_to_mp3(file_path):
        convert_to_mp3(file_path)
    else:
        print("无需转码，直接使用原音频")


def list_formats(url, cookies_path=None):
    ydl_opts = {
        'listformats': True,
        'quiet': False,
    }

    if cookies_path and os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def progress_hook(d):
    if d.get('status') == 'downloading':
        print(
            f"\r下载中: {d.get('_percent_str','').strip()} "
            f"{d.get('_speed_str','')} "
            f"{d.get('_eta_str','')}",
            end=''
        )


def main():
    if len(sys.argv) < 3:
        print("用法: python xxx.py <url> list|audio")
        return

    url = sys.argv[1]
    action = sys.argv[2]

    cookies_path = 'www.youtube.com_cookies.txt'

    if action == 'list':
        list_formats(url, cookies_path)

    elif action == 'audio':
        fmt = sys.argv[3] if len(sys.argv) > 3 else 'bestaudio'
        download_audio(url, cookies_path, fmt)

    else:
        print("仅支持 list / audio")


if __name__ == '__main__':
    main()