import yt_dlp
import os
from datetime import datetime

class VideoDownloader:
    def __init__(self):
        # 创建输出目录
        self.output_dir = 'out'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # 基本下载配置
        self.ydl_opts = {
            'format': 'best',  # 下载最佳质量
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),  # 输出模板
            'quiet': False,  # 显示下载进度
            'no_warnings': True,
            'progress_hooks': [self._progress_hook]  # 进度回调
        }
    
    def _progress_hook(self, d):
        """下载进度回调"""
        if d['status'] == 'downloading':
            # 计算下载进度
            if 'total_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                print(f"\r下载进度: {percent:.1f}%", end='', flush=True)
            elif 'downloaded_bytes' in d:
                print(f"\r已下载: {d['downloaded_bytes'] / 1024 / 1024:.1f}MB", end='', flush=True)
        elif d['status'] == 'finished':
            print("\n下载完成！")
    
    def check_video(self, video_url):
        """检查视频信息"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return {
                    'supported': True,
                    'title': info.get('title', 'unknown_video'),
                    'platform': info.get('extractor', 'unknown_platform'),
                    'duration': info.get('duration', 0),
                    'formats': info.get('formats', []),
                    'error': None
                }
        except Exception as e:
            return {
                'supported': False,
                'error': str(e)
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
    
    def download_video(self, video_url, quality='best'):
        """下载视频"""
        try:
            # 检查视频信息
            info = self.check_video(video_url)
            if not info['supported']:
                print(f"不支持此视频下载: {info['error']}")
                return False
            
            # 打印视频信息
            print(f"\n视频信息:")
            print(f"标题: {info['title']}")
            print(f"平台: {info['platform']}")
            print(f"时长: {self.format_duration(info['duration'])}")
            
            # 根据质量选择下载格式
            if quality != 'best':
                # 这里可以添加质量选择逻辑
                pass
            
            # 开始下载
            print("\n开始下载视频...")
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([video_url])
            
            return True
            
        except Exception as e:
            print(f"下载出错: {str(e)}")
            return False

def main():
    downloader = VideoDownloader()
    
    while True:
        print("\n视频下载演示")
        print("1. 下载单个视频")
        print("2. 查看视频信息")
        print("3. 退出")
        
        choice = input("\n请选择操作 (1-3): ").strip()
        
        if choice == '1':
            url = input("\n请输入视频URL: ").strip()
            if downloader.download_video(url):
                print("\n下载完成，文件保存在out目录")
            else:
                print("\n下载失败")
                
        elif choice == '2':
            url = input("\n请输入视频URL: ").strip()
            info = downloader.check_video(url)
            if info['supported']:
                print(f"\n视频信息:")
                print(f"标题: {info['title']}")
                print(f"平台: {info['platform']}")
                print(f"时长: {downloader.format_duration(info['duration'])}")
            else:
                print(f"\n获取视频信息失败: {info['error']}")
                
        elif choice == '3':
            print("\n程序已退出")
            break
            
        else:
            print("\n无效的选择，请重试")

if __name__ == "__main__":
    main() 