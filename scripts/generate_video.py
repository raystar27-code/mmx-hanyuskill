import argparse
import os
import subprocess
import sys
from parser import TextParser
from renderer import VideoFrameRenderer
from minimax_client import MiniMaxClient

def main():
    parser = argparse.ArgumentParser(description="中韩高亮朗读视频生成器")
    parser.add_argument("--text", help="输入的中文文本内容")
    parser.add_argument("--file", help="输入的文本文件路径（支持单语或中韩对照）")
    parser.add_argument("--bilingual", action="store_true", help="声明输入为中韩对照双语格式（每行: 中文 | 韩文），将跳过大模型翻译")
    parser.add_argument("--voice", choices=["female", "male"], default="female", help="声音类型 (默认女声 female，男声 male)")
    parser.add_argument("--output", default="output.mp4", help="输出视频文件名（默认 output.mp4）")
    args = parser.parse_args()
    
    # 1. 获取文本
    text = ""
    if args.file:
        if not os.path.exists(args.file):
            print(f"错误: 输入文件 {args.file} 不存在！", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("错误: 必须提供 --text 或 --file 参数中的一个！", file=sys.stderr)
        sys.exit(1)
        
    text = text.strip()
    if not text:
        print("错误: 输入文本不能为空！", file=sys.stderr)
        sys.exit(1)
        
    # 2. 解析与翻译
    text_parser = TextParser()
    client = MiniMaxClient()
    
    if args.bilingual:
        pairs = text_parser.parse(text, is_bilingual=True)
    else:
        print("正在调用 MiniMax 翻译中文文本为韩文...")
        translated = client.translate(text)
        if not translated:
            print("错误: 翻译失败或返回为空！", file=sys.stderr)
            sys.exit(1)
        pairs = text_parser.parse(translated, is_bilingual=True)
        
    if not pairs:
        # 如果是单语模式且翻译返回不带'|'的纯韩文，我们做一个防御性回退
        # 尝试将原文 and 译文按句自动配对
        if not args.bilingual:
            zh_sentences = text_parser.split_sentences(text)
            ko_sentences = text_parser.split_sentences(translated)
            # 过滤掉空的
            zh_sentences = [s for s in zh_sentences if s.strip()]
            ko_sentences = [s for s in ko_sentences if s.strip()]
            if len(zh_sentences) == len(ko_sentences):
                pairs = list(zip(zh_sentences, ko_sentences))
                
    if not pairs:
        print("错误: 无法解析或对齐中文与韩文句子，请检查格式或确保翻译输出正常！", file=sys.stderr)
        if not args.bilingual:
            print(f"MiniMax 翻译输出为：\n{translated}", file=sys.stderr)
        sys.exit(1)
        
    print(f"已成功解析出 {len(pairs)} 组句子，开始生成单句音视频片段...")
    
    # 创建临时工作目录
    temp_dir = "temp_segments"
    os.makedirs(temp_dir, exist_ok=True)
    
    segment_files = []
    renderer = VideoFrameRenderer()
    
    try:
        # 逐句生成
        for idx, (zh, ko) in enumerate(pairs):
            print(f"正在生成第 {idx+1}/{len(pairs)} 句...")
            
            # 生成高亮图片
            img_path = os.path.join(temp_dir, f"frame_{idx}.png")
            renderer.render(pairs, idx, img_path)
            
            # 生成 TTS 音频
            audio_path = os.path.join(temp_dir, f"audio_{idx}.mp3")
            success = client.synthesize(ko, args.voice, audio_path)
            if not success or not os.path.exists(audio_path):
                print(f"错误: 第 {idx+1} 句音频合成失败！", file=sys.stderr)
                sys.exit(1)
                
            # 合成单句短视频段
            segment_mp4 = os.path.join(temp_dir, f"segment_{idx}.mp4")
            cmd_segment = [
                "ffmpeg", "-y", "-loop", "1", "-i", img_path, "-i", audio_path,
                "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac",
                "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", segment_mp4
            ]
            subprocess.run(cmd_segment, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            segment_files.append(segment_mp4)
            
        if not segment_files:
            print("错误: 没有成功合成任何单句视频段！", file=sys.stderr)
            sys.exit(1)
            
        # 拼接视频
        concat_txt_path = os.path.join(temp_dir, "concat.txt")
        with open(concat_txt_path, "w", encoding="utf-8") as f:
            for seg in segment_files:
                f.write(f"file '{os.path.abspath(seg)}'\n")
                
        print("正在拼接各片段以生成最终视频...")
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_path,
            "-c", "copy", args.output
        ]
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"🎉 视频生成成功！输出文件: {args.output}")
        
    finally:
        # 清理临时文件
        print("正在清理临时缓存...")
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except Exception:
                    pass
            try:
                os.rmdir(temp_dir)
            except Exception:
                pass

if __name__ == "__main__":
    main()
