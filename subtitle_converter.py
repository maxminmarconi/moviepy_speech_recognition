import os
import re
from datetime import datetime

class SubtitleConverter:
    def __init__(self):
        self.supported_formats = ['.srt', '.txt', '.vtt']
    
    def is_timestamp_line(self, line):
        """检查是否为时间轴行"""
        line = line.strip()
        # 匹配 SRT 格式时间轴: 00:00:00,000 --> 00:00:00,000
        srt_pattern = r'^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}$'
        # 匹配 VTT 格式时间轴: 00:00:00.000 --> 00:00:00.000
        vtt_pattern = r'^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}$'
        # 匹配简单时间格式: [00:00] 或 (01:23)
        simple_pattern = r'^\[?\(?\d{2}:\d{2}\]?\)?$'
        
        return bool(
            re.match(srt_pattern, line) or 
            re.match(vtt_pattern, line) or 
            re.match(simple_pattern, line)
        )
    
    def is_index_line(self, line):
        """检查是否为序号行"""
        return line.strip().isdigit()
    
    def extract_pure_text(self, input_file, output_file=None):
        """从字幕文件中提取纯文本"""
        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"找不到输入文件: {input_file}")
            
            # 获取文件扩展名
            file_ext = os.path.splitext(input_file)[1].lower()
            if file_ext not in self.supported_formats:
                raise ValueError(f"不支持的文件格式: {file_ext}")
            
            # 如果没有指定输出文件，自动生成输出文件名
            if not output_file:
                base_name = os.path.splitext(input_file)[0]
                output_file = f"{base_name}_纯文本.txt"
            
            pure_text_lines = []
            current_text = []
            
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            skip_next_line = False
            for i, line in enumerate(lines):
                line = line.strip()
                
                # 跳过空行、序号行和时间轴行
                if (not line or 
                    self.is_index_line(line) or 
                    self.is_timestamp_line(line) or
                    skip_next_line):  # 跳过WEBVTT标记后的行
                    if line == 'WEBVTT':
                        skip_next_line = True
                    else:
                        skip_next_line = False
                    if current_text:
                        # 合并多行文本，去除多余空格
                        text = ' '.join(current_text)
                        # 去除特殊标记，如<c>等
                        text = re.sub(r'<[^>]+>', '', text)
                        pure_text_lines.append(text)
                        current_text = []
                    continue
                
                # 去除特殊标记
                line = re.sub(r'<[^>]+>', '', line)
                if line:
                    current_text.append(line)
            
            # 处理最后一组文本
            if current_text:
                text = ' '.join(current_text)
                text = re.sub(r'<[^>]+>', '', text)
                pure_text_lines.append(text)
            
            # 写入输出文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(pure_text_lines))
            
            return {
                'success': True,
                'input_file': input_file,
                'output_file': output_file,
                'lines_count': len(pure_text_lines)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'input_file': input_file
            }
    
    def batch_convert(self, input_dir, output_dir=None):
        """批量转换目录下的所有字幕文件"""
        if not os.path.exists(input_dir):
            return {'success': False, 'error': f"输入目录不存在: {input_dir}"}
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        results = []
        for file in os.listdir(input_dir):
            if os.path.splitext(file)[1].lower() in self.supported_formats:
                input_file = os.path.join(input_dir, file)
                if output_dir:
                    base_name = os.path.splitext(file)[0]
                    output_file = os.path.join(output_dir, 
                                             f"{base_name}_纯文本_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                else:
                    output_file = None
                
                result = self.extract_pure_text(input_file, output_file)
                results.append(result)
        
        return results

def main():
    converter = SubtitleConverter()
    
    while True:
        print("\n字幕转换工具")
        print("1. 转换单个文件")
        print("2. 批量转换目录")
        print("3. 退出")
        
        choice = input("\n请选择操作 (1-3): ").strip()
        
        if choice == '1':
            input_file = input("\n请输入字幕文件路径: ").strip()
            result = converter.extract_pure_text(input_file)
            
            if result['success']:
                print(f"\n转换成功！")
                print(f"输入文件: {result['input_file']}")
                print(f"输出文件: {result['output_file']}")
                print(f"提取行数: {result['lines_count']}")
            else:
                print(f"\n转换失败: {result['error']}")
                
        elif choice == '2':
            input_dir = input("\n请输入字幕文件目录: ").strip()
            output_dir = input("请输入输出目录（可选，直接回车使用原目录）: ").strip()
            
            results = converter.batch_convert(input_dir, output_dir if output_dir else None)
            
            print("\n转换结果:")
            for result in results:
                if result['success']:
                    print(f"\n成功: {result['input_file']}")
                    print(f"输出: {result['output_file']}")
                    print(f"行数: {result['lines_count']}")
                else:
                    print(f"\n失败: {result['input_file']}")
                    print(f"错误: {result['error']}")
                    
        elif choice == '3':
            print("\n程序已退出")
            break
        else:
            print("\n无效的选择，请重试")

if __name__ == "__main__":
    main() 