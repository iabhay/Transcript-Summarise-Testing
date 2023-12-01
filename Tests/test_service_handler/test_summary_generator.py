import pytest
from unittest.mock import Mock, patch
from src.service_handler.summary_handler.sum_gen import SummaryGenerator


def test_summary_generator_successful(mocker):
    mock_summary = mocker.MagicMock()
    mock_output = mocker.MagicMock()
    mock_pipeline = mocker.MagicMock()
    mocker.patch('oneai.Pipeline', mock_pipeline)
    mock_pipeline().run.return_value = mock_output
    mock_output.summary.text = "This is a test input for summarization."    
    # Instance of SummaryGenerator
    summary_gen = SummaryGenerator()

    # Input text for summary generation
    input_text = "This is a test input for summarization."

    # Call the summary generator method
    summary = summary_gen.summary_generator(input_text)

    # Check if summary is generated correctly
    assert summary == "This is a test input for summarization."


def test_summary_generator_failure(mocker):
    mock_pipeline = mocker.MagicMock()
    mocker.patch('oneai.Pipeline', mock_pipeline)
    mock_pipeline().run.side_effect = Exception('Some_info')

    # Initialize SummaryGenerator
    summary_gen = SummaryGenerator()

    # Call the summary_generator method with None input (to trigger the exception)
    summary = summary_gen.summary_generator("hjaks")
    assert summary is None
