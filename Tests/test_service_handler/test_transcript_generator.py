from unittest.mock import Mock
import pytest
from src.service_handler.transcript_handler.transcript_generator import transcriptor
import textwrap
transcriptor = transcriptor()
func = transcriptor.extract_video_id


def mock_func_throw(*args, **kwargs):
    raise Exception("Some_info")

def test_transcript_fail(monkeypatch):
    monkeypatch.setattr('src.service_handler.transcript_handler.transcript_generator.YouTubeTranscriptApi.get_transcript', mock_func_throw)
    val = transcriptor.get_transcript("12345678910gfgfh")
    assert val is None

def test_transcript_pass(monkeypatch):
    monkeypatch.setattr('src.service_handler.transcript_handler.transcript_generator.YouTubeTranscriptApi.get_transcript', lambda _: "Good API")
    val = transcriptor.get_transcript("12345678910gfgfh")
    assert val == "Good API"
    
def test_extract_video_id():
    val = func("12345678910gfgfh")
    assert val == "678910gfgfh"

def test_extract_video_id_fail():
    val = func("12345678910gfgfh")
    assert val != "12345678910gfgfh"


def test_format_transcript_pass(monkeypatch):
    monkeypatch.setattr(transcriptor, 'get_transcript',lambda _:[{"text":"Zol API"}, {"text": "Lol API"}])
    assert transcriptor.format_transcript("12345678910gfgfh") == "Zol API\nLol API\n"
    

def test_format_transcript_fail(monkeypatch):
    monkeypatch.setattr(transcriptor, 'get_transcript',lambda _: None)
    assert transcriptor.format_transcript("12345678910gfgfh") == None