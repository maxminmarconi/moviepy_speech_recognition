import yt_dlp
import os
from datetime import datetime
from subtitle_converter import SubtitleConverter
from youtube_comments_extractor import YouTubeCommentsExtractor

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
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.converter = SubtitleConverter()
        self.comments_extractor = YouTubeCommentsExtractor(self.timestamp)  # 添加评论提取器
        # 创建输出目录
        self.output_dir = 'out'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def save_file(self, content, filename, ext='.txt'):
        """统一的文件保存方法"""
        output_file = os.path.join(self.output_dir, f"{filename}_{self.timestamp}{ext}")
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
    
    def save_combined_output(self, video_info, subtitle_text, comments):
        """保存合并的字幕和评论信息"""
        output_file = os.path.join(self.output_dir, f"{video_info['id']}_完整内容_{self.timestamp}.txt")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # 写入字幕内容
                if subtitle_text:
                    f.write("=" * 50 + "\n")
                    f.write("字幕内容\n")
                    f.write("=" * 50 + "\n")
                    f.write(subtitle_text + "\n\n")
                
                # 写入评论信息
                if comments:
                    f.write("评论统计:\n")
                    f.write(f"评论总数: {comments.get('comments_count', 0)}\n\n")
                
                # 写入评论内容
                if comments and 'comments' in comments:
                    f.write("=" * 50 + "\n")
                    f.write("评论内容\n")
                    f.write("=" * 50 + "\n")
                    for comment in comments['comments']:
                        f.write(f"作者: {comment['author']}\n")
                        f.write(f"时间: {comment['time']}\n")
                        f.write(f"内容: {comment['text']}\n")
                        if comment.get('like_count'):
                            f.write(f"点赞: {comment['like_count']}\n")
                        if comment.get('reply_count'):
                            f.write(f"回复数: {comment['reply_count']}\n")
                        f.write("-" * 50 + "\n")
            
            return output_file
        except Exception as e:
            print(f"保存合并内容时发生错误: {str(e)}")
            return None
    
    def extract_subtitles(self, video_url):
        """提取视频字幕和评论"""
        try:
            # 一次性检查视频支持和字幕信息
            video_info = self.check_video(video_url)
            if not video_info['supported']:
                print(f"\n不支持此视频下载: {video_info['error']}")
                return None
            
            self._print_video_info(video_info)
            self._print_subtitle_info(video_info)
            
            result = {
                'subtitles': None,
                'comments': None,
                'combined': None  # 添加合并输出的结果
            }
            
            # 检查字幕可用性
            if not video_info['manual_subtitles'] and not video_info['auto_subtitles']:
                print("\n该视频没有任何可用字幕！")
            else:
                # 优先使用手动字幕，其次是自动字幕
                lang_code = None
                for code in ['en','zh', 'zh-Hans']:
                    if code in video_info['manual_subtitles']:
                        lang_code = code
                        break
                    elif code in video_info['auto_subtitles']:
                        lang_code = code
                        break
                
                self.ydl_opts['subtitleslangs'] = [lang_code]
                
                # 下载字幕
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([video_url])
                print("\n下载字幕结束，开始本地处理")

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
                        result['subtitles'] = {
                            'original': original_file,
                            'pure_text': pure_text['output_file']
                        }
                        print(f"\n字幕已保存:")
                        print(f"原始字幕: {original_file}")
                        print(f"纯文本字幕: {pure_text['output_file']}")
                else:
                    print("\n无法找到下载的字幕文件")
            
            # 读取纯文本字幕内容
            subtitle_text = None
            if result['subtitles'] and 'pure_text' in result['subtitles']:
                try:
                    with open(result['subtitles']['pure_text'], 'r', encoding='utf-8') as f:
                        subtitle_text = f.read()
                except Exception as e:
                    print(f"读取字幕文件时发生错误: {str(e)}")
            
            # 获取评论
            print("\n开始获取评论...")
            comments = self.comments_extractor.extract_comments(video_url)
            if comments:
                result['comments'] = comments
                print(f"\n评论已保存:")
                print(f"文本文件: {comments['txt_file']}")
                print(f"JSON文件: {comments['json_file']}")
                print(f"评论数量: {comments['comments_count']}")
            else:
                print("\n无法获取评论")
            
            # 合并输出
            if subtitle_text or comments:
                print("\n正在生成完整内容文件...")
                combined_file = self.save_combined_output(video_info, subtitle_text, comments)
                if combined_file:
                    result['combined'] = combined_file
                    print(f"完整内容已保存到: {combined_file}")
            
            return result
            
        except Exception as e:
            print(f"处理视频时发生错误: {str(e)}")
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
        
        # 提取字幕和评论
        result = extractor.extract_subtitles(video_url)
        
        if not result or (not result['subtitles'] and not result['comments']):
            print("\n无法获取任何内容")
        elif result['combined']:
            print(f"\n所有内容已合并保存到: {result['combined']}")

if __name__ == "__main__":
    main() 