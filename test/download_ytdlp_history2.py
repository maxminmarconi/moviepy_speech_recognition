import os
import yt_dlp

def download_youtube(url, lang="zh-Hans", audio_only=False):
    """
    下载 YouTube 视频/音频 + 字幕
    :param url: YouTube 视频链接
    :param lang: 字幕语言（默认英文），比如 "en", "zh-Hans", "all"
    :param audio_only: 是否只提取音频（默认 False）
    """
    # 下载配置
    ydl_opts = {
        "format": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]",
        "merge_output_format": "mp4",
        "outtmpl": "videos/%(title)s.%(ext)s",
        "writesubtitles": True,
        "embedsubtitles": True,
        "subtitleslangs": ["zh-Hans"],
        "subtitlesformat": "srt",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
    }


    if audio_only:
        # 下载后转 mp3
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        })

    # 执行下载
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    # 示例
    video_url = "https://www.youtube.com/watch?v=FPZwFMrIlsk"  # 替换成你的视频链接

    # 1. 下载视频 + 英文字幕 
    download_youtube(video_url, lang="zh-Hans", audio_only=False)

    # 2. 下载音频(mp3) + 中文字幕
    # download_youtube(video_url, lang="zh-Hans", audio_only=True)