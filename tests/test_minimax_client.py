from unittest.mock import patch, MagicMock
from scripts.minimax_client import MiniMaxClient

@patch('subprocess.run')
def test_translate_text(mock_run):
    mock_run.return_value = MagicMock(stdout="今天天气真好。 | 오늘 날씨가 정말 좋네요.", returncode=0)
    client = MiniMaxClient()
    translation = client.translate("今天天气真好。")
    assert "오늘" in translation
    
@patch('subprocess.run')
def test_synthesize_tts(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    client = MiniMaxClient()
    success = client.synthesize("오늘 날씨가 정말 좋네요.", "female", "tests/output.mp3")
    assert success is True
