import pytest
from unittest.mock import mock_open, patch
from src.users.submittedvideo.video_service import VideoService

@pytest.fixture(autouse=True)
def video_service_fixture(mocker):


    mock_transcript = mocker.MagicMock()
    mocker.patch('src.users.submittedvideo.video_service.transcriptor', return_value=mock_transcript)


    mock_cotent_checker = mocker.MagicMock()
    mocker.patch('src.users.submittedvideo.video_service.ContentChecker', return_value=mock_cotent_checker)


    mock_ban_url = mocker.MagicMock()
    mocker.patch('src.users.submittedvideo.video_service.BanUrlDB', mock_ban_url)


    mock_searches_db = mocker.MagicMock()
    mocker.patch('src.users.submittedvideo.video_service.SearchesDB', mock_searches_db)


    mock_summary_generator = mocker.MagicMock()
    mocker.patch('src.users.submittedvideo.video_service.SummaryGenerator', return_value=mock_summary_generator)


    mock_history_db = mocker.MagicMock()
    mocker.patch('src.users.submittedvideo.video_service.HistoryDB', mock_history_db)


    mock_premium_listing_db = mocker.MagicMock()
    mocker.patch('src.users.submittedvideo.video_service.PremiumListingsDB', mock_premium_listing_db)

    mock_history_db.save_history.return_value = True

    mock_ban_url.save_ban_url.return_value = True

    mock_transcript.extract_video_id.return_value = True

    mock_transcript.format_transcript.return_value = "Transcript"
    
    
    mock_summary_generator.summary_generator.return_value = "Summary"
    
    mock_fix_obj = VideoService("123")
    return mock_fix_obj

    
    


def test_show_video_details(video_service_fixture, mocker, capsys):
    video_service_fixture.show_video_details("Transcript heder", "Summary same here",123)
    captured = capsys.readouterr()
    assert "Video URLID - 123\nTranscript Length - 2\nSummary Length - 3\n" == captured.out

def test_save_transcript(video_service_fixture, mocker, capsys):
    with patch('builtins.open', mock_open()):
    #  with mocker.patch('builtins.open', mocker.mock_open):
        with open("Tests/test_files/transcript.txt", "w+", encoding="utf-8") as file_mock:
            file_mock.write("Transcript")
        video_service_fixture.save_transcript("Transcript heder",123)
        captured = capsys.readouterr()
        assert "Transcript File Generated with id - 123\n" == captured.out
       
def test_submitted_video_module(video_service_fixture,mocker,capsys):
    inps = iter([1,2,3,5,4])
    mocker.patch('builtins.input', lambda _: next(inps))
    mocker.patch('src.users.submittedvideo.video_service.Config.AFTER_SUBMITTING_URL_PROMPT_LENGTH', 4)
    mocker.patch('src.users.submittedvideo.video_service.Config.EXITING_PROMPT', "Exiting")
    mocker.patch('src.users.submittedvideo.video_service.Config.INVALID_INPUT_PROMPT', "Invalid")
    mocker.patch.object(VideoService,'save_summary')
    mocker.patch.object(VideoService,'save_transcript')
    mocker.patch.object(VideoService,'show_video_details')
    video_service_fixture.submitted_video_module("Transcript heder", "Summary same here",123)
    captured = capsys.readouterr()
    assert "Invalid" in captured.out
    assert "Exiting" in captured.out



# def test_submit_video(mocker, video_service_fixture):
#     mocker.patch('builtins.input', return_value="https://www.youtube.com/watch?v=1")
#     mocker.patch('src.users.submittedvideo.video_service.url_validation', return_value=True)


#     video_service_fixture.mock_premium_listing_db.check_premium_list_url.return_value = []
    
#     video_service_fixture.mock_searches_db.update_user_search_count.return_value = False
    
#     video_service_fixture.mock_ban_url.fetch_ban_url.return_value = True
    
    
    
#     video_service_fixture.mock_cotent_checker.analyze_text.return_value = {"Hate": 0, "Violence": 0, "Adult": 0}
    
    

    


#     assert video_service_fixture.submit_video() == False
   

# def test_submit_video2(mocker, video_service_fixture):
#     mocker.patch('builtins.input', return_value="https://www.youtube.com/watch?v=1")
#     mocker.patch('src.users.submittedvideo.video_service.url_validation', return_value=True)
#     video_service_fixture.mock_history_db.save_history.return_value = True

#     video_service_fixture.mock_premium_listing_db.check_premium_list_url.return_value = []
    
#     video_service_fixture.mock_searches_db.update_user_search_count.return_value = False
    
#     video_service_fixture.mock_ban_url.fetch_ban_url.return_value = False
    
#     video_service_fixture.mock_ban_url.save_ban_url.return_value = True
    
#     video_service_fixture.mock_cotent_checker.analyze_text.return_value = {"Hate": 0, "Violence": 0, "Adult": 0}
    
#     video_service_fixture.mock_transcript.extract_video_id.return_value = True

#     video_service_fixture.mock_transcript.format_transcript.return_value = "Transcript"
    
    
#     video_service_fixture.mock_summary_generator.summary_generator.return_value = "Summary"


#     assert video_service_fixture.submit_video() == True
