#!/usr/bin/env python3
# download_ytdlp.py
# 用法: python download_ytdlp.py "https://youtu.be/xxx" --path ./videos --format "bestvideo+bestaudio/best"
# 存在音频和字幕对不上的问题！！！

import argparse
import os
from yt_dlp import YoutubeDL

def download(url, out_path='.', ytdlp_opts=None):
    if ytdlp_opts is None:
        ytdlp_opts = {}

    ytdlp_opts_default = {
        'outtmpl': os.path.join(out_path, '%(title)s [%(id)s].%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',  # 合并输出格式
        'noplaylist': True,            # 默认不下载整个播放列表
        'quiet': False,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
    }
    # 合并用户自定义选项
    ytdlp_opts_default.update(ytdlp_opts)

    with YoutubeDL(ytdlp_opts_default) as ydl:
        result = ydl.download([url])
        return result

def progress_hook(d):
    status = d.get('status')
    if status == 'downloading':
        # percentage 可能没有，有时提供 eta/ speed
        pct = d.get('pct')
        if pct:
            print(f"\r下载中: {pct:.1f}%  已下载 {d.get('downloaded_bytes',0)} bytes", end='', flush=True)
        else:
            print("\r下载中...", end='', flush=True)
    elif status == 'finished':
        print("\n已下载完成，开始合并/处理文件...")
    elif status == 'error':
        print("\n下载出错:", d)

def main():
    parser = argparse.ArgumentParser(description="使用 yt-dlp 下载视频")
    parser.add_argument("url", help="视频或播放列表 URL")
    parser.add_argument("--path", "-p", default=".", help="保存目录")
    parser.add_argument("--format", "-f", default="bestvideo+bestaudio/best", help="下载格式，yt-dlp 格式字符串")
    parser.add_argument("--playlist", action="store_true", help="允许下载播放列表")
    args = parser.parse_args()

    opts = {
        'format': args.format,
        'outtmpl': os.path.join(args.path, '%(title)s [%(id)s].%(ext)s'),
        'noplaylist': not args.playlist,
        'merge_output_format': 'mp4',
    }

    download(args.url, out_path=args.path, ytdlp_opts=opts)

if __name__ == "__main__":
    main()
