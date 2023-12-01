import pytest
import sys
from src.service_handler.content_checker.content_check import ContentChecker

# @pytest.mark.skip
def test_content_check_success(mocker):
    
    mock_client = mocker.MagicMock()
    mocker.patch('src.service_handler.content_checker.content_check.ContentSafetyClient', return_value=mock_client)
    
    mock_req = mocker.MagicMock()
    mocker.patch('src.service_handler.content_checker.content_check.AnalyzeTextOptions', return_value=mock_req)
    
    mock_res = mocker.MagicMock()
    mock_client.analyze_text.return_value = mock_res
    
    mock_hate_result = mocker.MagicMock()
    mock_hate_result.severity = 0
    
    mock_self_harm_result = mocker.MagicMock()
    mock_self_harm_result.severity = 1
    
    mock_sexual_result = mocker.MagicMock()
    mock_sexual_result.severity = 1
    
    mock_violence_result = mocker.MagicMock()
    mock_violence_result.severity = 1
    
    mock_res.hate_result = mock_hate_result
    mock_res.self_harm_result = mock_self_harm_result
    mock_res.sexual_result = mock_sexual_result
    mock_res.violence_result = mock_violence_result
    

    content_checker = ContentChecker()
    assert content_checker.analyze_text("test") == {"Hate": 0, "SelfHarm": 1, "Adult": 1, "Violence": 1}

# @pytest.fixture
# def content_checker(mocker):
#     # Mocking ContentSafetyClient and its methods
#     return ContentChecker()

# def test_analyze_text_success(content_checker, mocker):
#     # Mocking ContentSafetyClient instance and its analyze_text method
#     mocked_client = mocker.Mock()
#     mocked_client.analyze_text.return_value = mocker.Mock(
#         Hate=mocker.Mock(severity=1),
#         selfHarm=mocker.Mock(severity=2),
#         Adult=mocker.Mock(severity=3),
#         Violence=mocker.Mock(severity=4)
#     )
    
#     mocker.patch('src.service_handler.content_checker.content_check.ContentSafetyClient', lambda a, b: mocked_client)  # Replace the instance with the mocked one

#     # Call the analyze_text function
#     text = "Test"
#     result = content_checker.analyze_text(text)
#     mock_req = mocker.MagicMock()
#     mocker.patch('src.service_handler.content_checker.content_check.AnalyzeTextOptions', lambda _: mock_req)
#     # Assertions
#     mocked_client.analyze_text.assert_called_once_with(mock_req(text=text[:10000]))
#     assert result == {
#         "Hate": 1,
#         "SelfHarm": 2,
#         "Adult": 3,
#         "Violence": 4
#     }

# # def test_analyze_text_failure(content_checker, mocker):
# #     # Mocking ContentSafetyClient instance and simulate analyze_text failure
# #     mocked_client = mocker.Mock()
# #     mocked_client.analyze_text.side_effect = Exception("Mocked exception")
# #     content_checker.client = mocked_client  # Replace the instance with the mocked one

# #     # Call the analyze_text function
# #     text = "Your sample text goes here..."
# #     result = content_checker.analyze_text(text)

# #     # Assertions
# #     mocked_client.analyze_text.assert_called_once_with(AnalyzeTextOptions(text=text[:10000]))
# #     assert result is False
