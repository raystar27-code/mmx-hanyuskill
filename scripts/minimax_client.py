import subprocess
import sys

class MiniMaxClient:
    def translate(self, text):
        prompt = (
            "你是一个专业的中韩翻译助手。请将以下中文翻译为韩文。请严格按照'中文 | 韩文'的格式逐行输出，"
            "句子之间用换行符分隔。不要输出任何其他无关的解释或标点符号。\n"
            f"输入：{text}"
        )
        # 调用 mmx text chat 命令并强制纯文本输出
        cmd = ["mmx", "text", "chat", "--prompt", prompt, "--non-interactive", "--output", "text"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"翻译失败: {result.stderr}", file=sys.stderr)
            return ""
        return result.stdout.strip()
        
    def synthesize(self, text, voice_type, output_path):
        # 映射音色
        if voice_type == "female":
            voice_id = "Korean_SweetGirl"
        elif voice_type == "male":
            voice_id = "Korean_CalmGentleman"
        else:
            voice_id = voice_type  # 允许直接传入其他音色名称，如 Korean_CheerfulBoyfriend
            
        # 使用 mmx speech synthesize 生成音频
        cmd = ["mmx", "speech", "synthesize", "--text", text, "--voice", voice_id, "--out", output_path, "--non-interactive"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"TTS 生成失败: {result.stderr}", file=sys.stderr)
            return False
        return True
