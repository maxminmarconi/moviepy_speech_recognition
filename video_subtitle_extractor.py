import yt_dlp
import os
from datetime import datetime
from subtitle_converter import SubtitleConverter

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
        self.converter = SubtitleConverter()
        # 创建输出目录
        self.output_dir = 'out'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def save_file(self, content, filename, ext='.txt'):
        """统一的文件保存方法"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(self.output_dir, f"{filename}_{timestamp}{ext}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return output_file
    
    def check_video(self, video_url):
        """检查视频支持情况和字幕信息"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # 一次性获取所有信息
                info = ydl.extract_info(video_url, download=False)
                
                # 获取字幕信息
                has_manual_subs = info.get('subtitles', {})
                has_auto_subs = info.get('automatic_captions', {})
                
                return {
                    'supported': True,
                    'id': info.get('id', 'unknown_id'),
                    'title': info.get('title', 'unknown_video'),
                    'platform': info.get('extractor', 'unknown_platform'),
                    'duration': info.get('duration', 0),
                    'webpage_url': info.get('webpage_url', ''),
                    'manual_subtitles': list(has_manual_subs.keys()) if has_manual_subs else [],
                    'auto_subtitles': list(has_auto_subs.keys()) if has_auto_subs else [],
                    'error': None
                }
                
        except yt_dlp.utils.DownloadError as e:
            return {
                'supported': False,
                'error': str(e),
                'title': None,
                'platform': None,
                'duration': None,
                'webpage_url': None,
                'manual_subtitles': [],
                'auto_subtitles': []
            }
        except Exception as e:
            return {
                'supported': False,
                'error': f"未知错误: {str(e)}",
                'title': None,
                'platform': None,
                'duration': None,
                'webpage_url': None,
                'manual_subtitles': [],
                'auto_subtitles': []
            }
    
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
    
    def extract_subtitles(self, video_url):
        """提取视频字幕"""
        try:
            # 一次性检查视频支持和字幕信息
            video_info = self.check_video(video_url)
            if not video_info['supported']:
                print(f"\n不支持此视频下载: {video_info['error']}")
                return None
            
            self._print_video_info(video_info)
            self._print_subtitle_info(video_info)
            
            # 检查字幕可用性
            if not video_info['manual_subtitles'] and not video_info['auto_subtitles']:
                print("\n该视频没有任何可用字幕！")
                return None

            # 优先使用手动字幕，其次是自动字幕
            lang_code = (video_info['manual_subtitles'] or video_info['auto_subtitles'])[0]
            self.ydl_opts['subtitleslangs'] = [lang_code]
            
            # 下载字幕
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([video_url])
            print("\下载字幕结束，开始本地处理")

            # 查找并处理字幕文件
            subtitle_file = self._find_subtitle_file()
            if subtitle_file:
                # 读取原始字幕
                with open(subtitle_file, 'r', encoding='utf-8') as f:
                    subtitle_content = f.read()
                
                # 保存原始字幕和纯文本字幕
                original_file = self.save_file(subtitle_content, 
                                            f"{video_info['id']}_原始字幕", 
                                            '.srt')
                
                # 使用字幕转换器提取纯文本
                pure_text = self.converter.extract_pure_text(original_file)
                if pure_text['success']:
                    # 删除临时文件
                    os.remove(subtitle_file)
                    return {
                        'original': original_file,
                        'pure_text': pure_text['output_file']
                    }
            
            print("\n无法找到下载的字幕文件")
            return None
            
        except Exception as e:
            print(f"提取字幕时发生错误: {str(e)}")
            return None
    
    def _print_video_info(self, info):
        """打印视频信息"""
        print(f"\n视频信息:")
        print(f"标题: {info['title']}")
        print(f"平台: {info['platform']}")
        print(f"时长: {self.format_duration(info['duration'])}")
    
    def _print_subtitle_info(self, info):
        """打印字幕信息"""
        print("\n可用的字幕:")
        print("手动字幕:", ', '.join(info['manual_subtitles']) if info['manual_subtitles'] else "无")
        print("自动字幕:", ', '.join(info['auto_subtitles']) if info['auto_subtitles'] else "无")
    
    def _find_subtitle_file(self):
        """查找下载的字幕文件"""
        for file in os.listdir():
            if file.endswith('.srt') or file.endswith('.vtt'):
                return file
        return None

def main():
    extractor = SubtitleExtractor()
    while True:
        video_url = input("\n请输入视频URL (输入q退出): ").strip()
        
        if video_url.lower() == 'q':
            print("程序已退出")
            break
        
        # 提取字幕
        output_files = extractor.extract_subtitles(video_url)
        
        if output_files:
            print(f"\n原始字幕已保存到文件: {output_files['original']}")
            print(f"纯文本字幕已保存到文件: {output_files['pure_text']}")
        else:
            print("\n无法提取字幕")
        
        break

if __name__ == "__main__":
    main() 