import sys
import yt_dlp

def download_youtube_video(url, cookies_path, fmt='137+140'):
    # 下载配置
    ydl_opts = {
        #'cookiefile': cookies_path,                # 指定 cookies 文件
        # 自动选择最佳视频和音频（合并为 mp4）
        #'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        #'format': '96+140',
        #'format': '137+140',
        'format': fmt,                             # 格式选择
        'merge_output_format': 'mp4',
        # 输出路径和文件名
        'outtmpl': 'videos/%(title)s.%(ext)s',
        # 显示进度
        'progress_hooks': [
            lambda d: print(f"[{d.get('status')}] {d.get('filename')}") if d.get('status') else None
        ],
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
    }

    # 执行下载
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def list_formats(url, cookies_path):
    """
    列出指定 YouTube 视频的所有可下载格式
    :param url: 视频链接
    :param cookies_path: cookies.txt 文件路径
    """
    ydl_opts = {
        'cookiefile': cookies_path,  # 指定 cookies 文件
        'listformats': True,         # 等价于命令行的 --list-formats
        'quiet': False,              # 显示输出
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    """
    用法：
      python download_ytdlp.py <url> list
      python download_ytdlp.py <url> download [format]

    例：
      python download_ytdlp.py https://www.youtube.com/watch?v=xxxx list
      python download_ytdlp.py https://www.youtube.com/watch?v=xxxx download "137+140"
    """
    if len(sys.argv) < 3:
        print(main.__doc__)
        sys.exit(1)

    url = sys.argv[1]
    action = sys.argv[2].lower()
    fmt = sys.argv[3] if len(sys.argv) > 3 else '137+140'

    cookies_path = r'E:\research\demo\moviepy_speech_recognition\www.youtube.com_cookies.txt'
    if action == 'list':
        list_formats(url, cookies_path)
    elif action == 'download':
        download_youtube_video(url, cookies_path, fmt)
    else:
        print("❌ 无效的操作，请使用 list 或 download")

if __name__ == '__main__':
     main()