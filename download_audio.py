import sys
import os
import yt_dlp


def download_audio(url, cookies_path=None, fmt='bestaudio'):
    """
    下载音频并转换为 MP3
    """

    os.makedirs("audios", exist_ok=True)

    ydl_opts = {
        # 音频格式
        'format': fmt,

        # 输出文件
        'outtmpl': 'audios/%(title)s.%(ext)s',

        # 转 MP3
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],

        # 进度显示
        'progress_hooks': [progress_hook],

        # 浏览器模拟
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


def list_formats(url, cookies_path=None):
    """
    查看所有格式
    """

    ydl_opts = {
        'listformats': True,
        'quiet': False,
    }

    if cookies_path and os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def progress_hook(d):

    status = d.get('status')

    if status == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '')
        eta = d.get('_eta_str', '')

        print(
            f"\r下载中: {percent} "
            f"速度:{speed} "
            f"剩余:{eta}",
            end=''
        )

    elif status == 'finished':
        print("\n下载完成，开始转换 MP3...")


def main():

    """
    用法：

    查看格式：
    python download_audio.py <url> list

    下载最佳音频：
    python download_audio.py <url> audio

    下载指定音频格式：
    python download_audio.py <url> audio 251

    示例：

    python download_audio.py \
    https://www.youtube.com/watch?v=xxxx \
    list

    python download_audio.py \
    https://www.youtube.com/watch?v=xxxx \
    audio

    python download_audio.py \
    https://www.youtube.com/watch?v=xxxx \
    audio 251
    """

    if len(sys.argv) < 3:
        print(main.__doc__)
        return

    url = sys.argv[1]
    action = sys.argv[2].lower()

    cookies_path = r'www.youtube.com_cookies.txt'

    if action == 'list':
        list_formats(url, cookies_path)

    elif action == 'audio':

        fmt = (
            sys.argv[3]
            if len(sys.argv) > 3
            else 'bestaudio'
        )

        download_audio(
            url,
            cookies_path,
            fmt
        )

    else:
        print("仅支持：list 或 audio")


if __name__ == '__main__':
    main()