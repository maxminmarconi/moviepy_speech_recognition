import yt_dlp
import os
from datetime import datetime

class SubtitleExtractor:
    def __init__(self):
        self.ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'srt',
            'skip_download': True,  # 只下载字幕，不下载视频
            'quiet': True,
            'no_warnings': True
        }
    
    def check_video_support(self, video_url):
        """检查视频是否支持下载"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                # 尝试获取视频信息
                info = ydl.extract_info(video_url, download=False)
                
                support_info = {
                    'supported': True,
                    'title': info.get('title', 'unknown_video'),
                    'platform': info.get('extractor', 'unknown_platform'),
                    'duration': info.get('duration', 0),
                    'webpage_url': info.get('webpage_url', ''),
                    'error': None
                }
                
                return support_info
                
        except yt_dlp.utils.DownloadError as e:
            return {
                'supported': False,
                'error': str(e),
                'platform': None,
                'title': None,
                'duration': None,
                'webpage_url': None
            }
        except Exception as e:
            return {
                'supported': False,
                'error': f"未知错误: {str(e)}",
                'platform': None,
                'title': None,
                'duration': None,
                'webpage_url': None
            }
    
    def check_subtitles(self, video_url):
        """检查视频是否有字幕"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                # 检查是否有内置字幕
                has_manual_subs = info.get('subtitles', {})
                # 检查是否有自动生成的字幕
                has_auto_subs = info.get('automatic_captions', {})
                
                subtitle_info = {
                    'title': info.get('title', 'unknown_video'),
                    'manual_subtitles': list(has_manual_subs.keys()) if has_manual_subs else [],
                    'auto_subtitles': list(has_auto_subs.keys()) if has_auto_subs else [],
                    'duration': info.get('duration', 0),
                    'platform': info.get('extractor', 'unknown_platform')
                }
                
                return subtitle_info
                
        except Exception as e:
            print(f"检查字幕时发生错误: {str(e)}")
            return None
    
    def format_duration(self, seconds):
        """格式化视频时长"""
        if not seconds:
            return "未知时长"
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒"
        elif minutes > 0:
            return f"{int(minutes)}分钟{int(seconds)}秒"
        else:
            return f"{int(seconds)}秒"
    
    def extract_subtitles(self, video_url, lang_code=None):
        """提取视频字幕"""
        try:
            # 首先检查视频是否支持
            support_info = self.check_video_support(video_url)
            if not support_info['supported']:
                print(f"\n不支持此视频下载: {support_info['error']}")
                return None
                
            print(f"\n视频信息:")
            print(f"标题: {support_info['title']}")
            print(f"平台: {support_info['platform']}")
            print(f"时长: {self.format_duration(support_info['duration'])}")
            
            # 检查字幕情况
            subtitle_info = self.check_subtitles(video_url)
            if not subtitle_info:
                print("无法获取字幕信息")
                return None
                
            print("\n可用的字幕:")
            print("手动字幕:", ', '.join(subtitle_info['manual_subtitles']) if subtitle_info['manual_subtitles'] else "无")
            print("自动字幕:", ', '.join(subtitle_info['auto_subtitles']) if subtitle_info['auto_subtitles'] else "无")
            
            # 如果指定了语言代码，更新配置
            if lang_code:
                self.ydl_opts['subtitleslangs'] = [lang_code]
                
            # 如果没有任何字幕，直接返回
            if not subtitle_info['manual_subtitles'] and not subtitle_info['auto_subtitles']:
                print("\n该视频没有任何可用字幕！")
                return None
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # 下载字幕
                ydl.download([video_url])
                
                # 查找下载的字幕文件
                subtitle_file = None
                for file in os.listdir():
                    if file.endswith('.srt'):
                        subtitle_file = file
                        break
                
                if subtitle_file:
                    # 读取字幕内容
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        subtitle_content = f.read()
                    
                    # 保存处理后的字幕
                    output_file = f"{subtitle_info['title']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(subtitle_content)
                    
                    # 删除原始字幕文件
                    os.remove(subtitle_file)
                    
                    return output_file
                
                print("\n无法找到下载的字幕文件")
                return None
                
        except Exception as e:
            print(f"提取字幕时发生错误: {str(e)}")
            return None

def main():
    extractor = SubtitleExtractor()
    while True:
        video_url = input("\n请输入视频URL (输入q退出): ").strip()
        
        if video_url.lower() == 'q':
            print("程序已退出")
            break
            
        # 首先检查视频是否支持
        support_info = extractor.check_video_support(video_url)
        if not support_info['supported']:
            print(f"\n不支持此视频下载: {support_info['error']}")
            continue
            
        print(f"\n视频信息:")
        print(f"标题: {support_info['title']}")
        print(f"平台: {support_info['platform']}")
        print(f"时长: {extractor.format_duration(support_info['duration'])}")
        
        # 检查字幕
        subtitle_info = extractor.check_subtitles(video_url)
        if subtitle_info:
            print("\n可用的字幕语言:")
            if subtitle_info['manual_subtitles']:
                print("手动字幕:", ', '.join(subtitle_info['manual_subtitles']))
            if subtitle_info['auto_subtitles']:
                print("自动字幕:", ', '.join(subtitle_info['auto_subtitles']))
                
            # 让用户选择语言
            lang_code = input("\n请输入想要下载的字幕语言代码（直接回车使用默认语言）: ").strip()
            
            # 提取字幕
            output_file = extractor.extract_subtitles(video_url, lang_code if lang_code else subtitle_info['manual_subtitles'])
            
            if output_file:
                print(f"\n字幕已保存到文件: {output_file}")
            else:
                print("\n无法提取字幕")
        else:
            print("\n无法获取视频信息")

if __name__ == "__main__":
    main() 