import yt_dlp
import os
from datetime import datetime
import json

class YouTubeCommentsExtractor:
    def __init__(self):
        # 创建输出目录
        self.output_dir = 'out'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # 基本配置
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # 不下载视频
            'getcomments': True,   # 获取评论
            'ignoreerrors': True,  # 忽略错误继续运行
        }
    
    def save_comments(self, comments, filename):
        """保存评论到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(self.output_dir, f"{filename}_评论_{timestamp}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for comment in comments:
                # 写入评论信息
                f.write(f"作者: {comment['author']}\n")
                f.write(f"时间: {comment['time']}\n")
                f.write(f"内容: {comment['text']}\n")
                if comment.get('like_count'):
                    f.write(f"点赞: {comment['like_count']}\n")
                if comment.get('reply_count'):
                    f.write(f"回复数: {comment['reply_count']}\n")
                f.write("-" * 50 + "\n")
        
        return output_file
    
    def save_comments_json(self, comments, filename):
        """保存评论到JSON文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(self.output_dir, f"{filename}_评论_{timestamp}.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        
        return output_file
    
    def format_timestamp(self, timestamp):
        """格式化时间戳"""
        if not timestamp:
            return "未知时间"
        try:
            from datetime import datetime
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return str(timestamp)
    
    def extract_comments(self, video_url):
        """提取视频评论"""
        try:
            print("\n正在获取视频信息...")
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # 获取视频信息
                info = ydl.extract_info(video_url, download=False)
                
                if not info:
                    print("无法获取视频信息")
                    return None
                
                video_id = info.get('id', 'unknown')
                title = info.get('title', 'unknown_video')
                
                print(f"\n视频信息:")
                print(f"标题: {title}")
                print(f"ID: {video_id}")
                
                # 获取评论
                print("\n正在获取评论...")
                comments = []
                
                if 'comments' in info:
                    for comment in info['comments']:
                        comment_data = {
                            'author': comment.get('author', '未知作者'),
                            'time': self.format_timestamp(comment.get('timestamp')),
                            'text': comment.get('text', ''),
                            'like_count': comment.get('like_count', 0),
                            'reply_count': comment.get('reply_count', 0)
                        }
                        comments.append(comment_data)
                
                if not comments:
                    print("未找到任何评论")
                    return None
                
                print(f"\n共获取到 {len(comments)} 条评论")
                
                # 保存评论
                txt_file = self.save_comments(comments, video_id)
                json_file = self.save_comments_json(comments, video_id)
                
                return {
                    'txt_file': txt_file,
                    'json_file': json_file,
                    'comments_count': len(comments)
                }
                
        except Exception as e:
            print(f"获取评论时发生错误: {str(e)}")
            return None

def main():
    extractor = YouTubeCommentsExtractor()
    
    while True:
        print("\nYouTube评论提取工具")
        video_url = input("\n请输入YouTube视频URL (输入q退出): ").strip()
        
        if video_url.lower() == 'q':
            print("程序已退出")
            break
        
        result = extractor.extract_comments(video_url)
        
        if result:
            print(f"\n评论已保存:")
            print(f"文本文件: {result['txt_file']}")
            print(f"JSON文件: {result['json_file']}")
            print(f"评论数量: {result['comments_count']}")
        else:
            print("\n无法获取评论")
        
        # 是否继续
        if input("\n是否继续？(y/n): ").lower() != 'y':
            print("程序已退出")
            break

if __name__ == "__main__":
    main() 