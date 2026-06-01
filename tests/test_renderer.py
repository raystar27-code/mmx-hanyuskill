import os
from scripts.renderer import VideoFrameRenderer

def test_text_wrapping():
    renderer = VideoFrameRenderer()
    text = "这是一个非常长非常长非常长的中文句子，需要测试它是否可以自动折行。"
    # 模拟一个默认的简单 font
    from PIL import ImageFont
    font = ImageFont.load_default()
    wrapped = renderer.wrap_text(text, font, max_width=100)
    assert len(wrapped) > 1
    
def test_render_frame():
    pairs = [
        ("今天天气真好。", "오늘 날씨가 정말 좋네요."),
        ("我们出去玩吧！", "우리 놀러 가요!")
    ]
    renderer = VideoFrameRenderer()
    output_path = "tests/test_frame.png"
    renderer.render(pairs, active_index=0, output_path=output_path)
    assert os.path.exists(output_path)
    if os.path.exists(output_path):
        os.remove(output_path)
