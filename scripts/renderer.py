import os
import sys
from PIL import Image, ImageDraw, ImageFont

class VideoFrameRenderer:
    def __init__(self):
        # 1. 设定本地项目资源的字体路径，中韩分离，支持跨平台 (Mac / Linux VPS)
        self.font_path_ko = "resources/font_ko.ttf"
        self.font_path_zh = "resources/font_zh.ttf"
        
        # 2. 自动下载机制：如果本地不存在，分别拉取最优雅匹配的中韩开源衬线字体包
        os.makedirs("resources", exist_ok=True)
        
        # A. 韩文 Noto/Naver 经典明朝 (Nanum Myeongjo) 字体
        if not os.path.exists(self.font_path_ko):
            font_url_ko = "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/nanummyeongjo/NanumMyeongjo-Regular.ttf"
            success_ko = False
            for attempt in range(3):
                print(f"正在下载完全开源的经典韩文 Batang/明朝体 (Nanum Myeongjo) [第 {attempt+1}/3 次尝试]...")
                try:
                    if os.path.exists(self.font_path_ko):
                        os.remove(self.font_path_ko)
                    import requests
                    headers = {"User-Agent": "Mozilla/5.0"}
                    r = requests.get(font_url_ko, headers=headers, stream=True, timeout=20)
                    r.raise_for_status()
                    with open(self.font_path_ko, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print("🎉 韩文字体下载成功！")
                    success_ko = True
                    break
                except Exception as e:
                    print(f"韩文字体下载失败: {e}", file=sys.stderr)
            if not success_ko:
                self.font_path_ko = "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf" if os.path.exists("/System/Library/Fonts/Supplemental/AppleMyungjo.ttf") else None
                
        # B. 中文经典艺术衬线体 (ZCOOL XiaoWei 站酷小薇体 - 与明朝体完美绝配且支持完整中文简体)
        if not os.path.exists(self.font_path_zh):
            font_url_zh = "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/zcoolxiaowei/ZCOOLXiaoWei-Regular.ttf"
            success_zh = False
            for attempt in range(3):
                print(f"正在下载完全开源的精美中文宋体/明体衬线字体 (ZCOOL XiaoWei) [第 {attempt+1}/3 次尝试]...")
                try:
                    if os.path.exists(self.font_path_zh):
                        os.remove(self.font_path_zh)
                    import requests
                    headers = {"User-Agent": "Mozilla/5.0"}
                    r = requests.get(font_url_zh, headers=headers, stream=True, timeout=20)
                    r.raise_for_status()
                    with open(self.font_path_zh, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print("🎉 中文字体下载成功！")
                    success_zh = True
                    break
                except Exception as e:
                    print(f"中文字体下载失败: {e}", file=sys.stderr)
            if not success_zh:
                self.font_path_zh = "/System/Library/Fonts/Supplemental/Songti.ttc" if os.path.exists("/System/Library/Fonts/Supplemental/Songti.ttc") else None

    def wrap_text(self, text, font, max_width):
        lines = []
        words = list(text)
        current_line = []
        for word in words:
            current_line.append(word)
            # 计算当前行宽度
            bbox = font.getbbox("".join(current_line))
            width = bbox[2] - bbox[0]
            if width > max_width:
                current_line.pop()
                lines.append("".join(current_line))
                current_line = [word]
        if current_line:
            lines.append("".join(current_line))
        return lines

    def render(self, pairs, active_index, output_path):
        # 1. 创建 1080x1920 暖阳米黄 (#FAF5E6) 高档手账背景
        img = Image.new('RGB', (1080, 1920), color='#FAF5E6')
        draw = ImageDraw.Draw(img)
        
        # 2. 绘制精致规律的淡灰色点阵 (Dot Grid Pattern)，每 40px 部署一个淡褐色小圆点
        dot_color = '#E6DCC8'
        for y in range(40, 1920, 40):
            for x in range(40, 1080, 40):
                draw.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=dot_color)
        
        # 载入高雅经典的中韩双语 Batang/宋体 衬线字体组合，恢复您最喜爱的黄金字号尺寸
        try:
            font_ko = ImageFont.truetype(self.font_path_ko, 48) # 韩语恢复至完美的 48px
            font_zh = ImageFont.truetype(self.font_path_zh, 36) # 中文恢复至完美的 36px
        except IOError:
            font_ko = ImageFont.load_default()
            font_zh = ImageFont.load_default()
            
        # 计算所有内容的总高度以全局垂直居中
        parsed_lines = []
        total_height = 0
        
        for idx, (zh, ko) in enumerate(pairs):
            ko_lines = self.wrap_text(ko, font_ko, 960)
            zh_lines = self.wrap_text(zh, font_zh, 960)
            
            parsed_lines.append({
                "ko_lines": ko_lines,
                "zh_lines": zh_lines,
                "is_active": (idx == active_index)
            })
            
            # 本段内的折行行间距保持紧凑（字号的 1.25 倍）：韩语 60px；中文 45px
            ko_height = len(ko_lines) * 60
            zh_height = len(zh_lines) * 45
            group_height = ko_height + 25 + zh_height # 本段内中韩垂直间距调回紧凑的 25px
            total_height += group_height
            
        total_height += (len(pairs) - 1) * 120 # 每一段与下一段之间的间距拉大到 120px (段落间距)，让大字号排版同样极具留白呼吸感
        
        # 起始垂直坐标
        start_y = (1920 - total_height) // 2
        
        # 3. 仅通过文字颜色对比实现高亮渲染
        current_y = start_y
        for group in parsed_lines:
            is_active = group["is_active"]
            
            # 高亮句采用深邃醒目的复古朱红/深咖啡色，非高亮句则是清淡且看得清的柔和卡其灰 (#C2B49A)
            color_ko = '#A03020' if is_active else '#C2B49A' # 复古朱红 vs 优雅淡卡其
            color_zh = '#483524' if is_active else '#C2B49A' # 深胡桃褐 vs 优雅淡卡其
            
            # 绘制韩文行，本句内紧凑折行 (60px)
            for line in group["ko_lines"]:
                draw.text((540, current_y), line, fill=color_ko, font=font_ko, anchor="mt")
                current_y += 60
                
            current_y += 25 # 组内中韩空隙 25px (本段中韩行距不用 2.0)
            
            # 绘制中文行，本句内紧凑折行 (45px)
            for line in group["zh_lines"]:
                draw.text((540, current_y), line, fill=color_zh, font=font_zh, anchor="mt")
                current_y += 45
                
            current_y += 120 # 每一段与下一段的行间距 (段落距) 120px
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
