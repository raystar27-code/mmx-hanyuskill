from scripts.parser import TextParser

def test_parse_bilingual_text():
    input_text = "今天天气真好。 | 오늘 날씨가 정말 좋네요.\n我们出去玩吧！ | 우리 놀러 가요!"
    parser = TextParser()
    result = parser.parse(input_text, is_bilingual=True)
    assert result == [
        ("今天天气真好。", "오늘 날씨가 정말 좋네요."),
        ("我们出去玩吧！", "우리 놀러 가요!")
    ]
    
def test_split_sentences():
    input_text = "今天天气真好。我们出去玩吧！"
    parser = TextParser()
    result = parser.split_sentences(input_text)
    assert result == ["今天天气真好。", "我们出去玩吧！"]
