# 视频字幕提取器

一个简单而强大的视频字幕提取和转换工具，支持多平台视频字幕提取和格式转换。

## 功能特点

- 🎯 支持多平台视频字幕提取
- 📝 自动检测并下载字幕
- 🌍 支持多语言字幕
- 💾 自动保存原始字幕和纯文本
- 🔄 字幕格式转换功能

## 快速开始

### 环境要求
- Python 3.6+
- pip 包管理器

### 安装步骤

1. 安装依赖：
```bash
pip install yt-dlp
```

2. 下载项目：
```bash
git clone https://github.com/maxminmarconi/video-subtitle-extractor.git
cd video-subtitle-extractor
```

### 使用方法

1. **提取视频字幕并转换字幕格式**
```bash
python video_subtitle_extractor.py
```

## 支持的平台

- YouTube
- Bilibili
- 抖音
- 西瓜视频
- 更多支持yt-dlp的平台...

## 字幕语言代码

常用语言代码参考：
```
zh-CN : 简体中文
zh-TW : 繁体中文
en    : 英语
ja    : 日语
ko    : 韩语
```

## 输出文件

所有文件将保存在`out`目录下：
- 原始字幕：`视频标题_原始字幕_时间戳.srt`
- 纯文本：`视频标题_纯文本_时间戳.txt`

## 常见问题

### 无法获取字幕？
- 检查视频是否有字幕
- 确认网络连接正常
- 验证URL是否正确

### 字幕显示乱码？
- 使用支持UTF-8的编辑器
- 尝试使用VSCode或Notepad++

### 下载速度慢？
- 检查网络连接
- 考虑使用代理服务器

## 更新日志

### v1.1.0 (2024-03-21)
- 优化网络请求，减少请求次数
- 增加字幕格式转换功能
- 统一文件保存位置
- 改进错误处理

### v1.0.0 (2024-03-20)
- 首次发布
- 基础字幕提取功能

## 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- 所有贡献者

---


如果这个仓库对你有帮助，欢迎 ⭐️ Star 支持！欢迎提问。如果这个仓库帮你解决了问题或者提供了思路，是否可以请失业的我乘坐一趟公交车：

<p align="center"><img src="buy-me-a-coffee-wechat.jpg" width="240" height="240
" alt="" /></p>