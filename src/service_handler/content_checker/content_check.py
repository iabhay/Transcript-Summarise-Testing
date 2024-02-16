"""Module for Content check functionality"""

import logging
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)


class ContentChecker:
    """
    Class for Checking content of transcript
    ...
    Methods:
    -------
    Constructor() -> Setting Endpoint and key of api from environment variables
    analyze_text() -> API called for fetching Content based categorisation of transcript.
    """

    def __init__(self) -> None:
        """
        Method to set API credentials using Environment Variables
        Parameter-> self
        Return Type -> None
        """
        self.endpoint = os.getenv("AI_ENDPOINT")
        self.key = AzureKeyCredential(os.getenv("AI_KEY"))

    def analyze_text(self, transcript: str) -> None:
        """
        Method to send API request categorise the transcript generated
        Parameter -> transcript: str
        Return Type -> dict
        """
        transcript = transcript[:10000]
        client = ContentSafetyClient(self.endpoint, self.key)
        request = AnalyzeTextOptions(text=transcript)
        try:
            response = client.analyze_text(request)
        except Exception:
            return False
        else:
            hate_result = next(
                item
                for item in response.categories_analysis
                if item.category == TextCategory.HATE
            )
            self_harm_result = next(
                item
                for item in response.categories_analysis
                if item.category == TextCategory.SELF_HARM
            )
            sexual_result = next(
                item
                for item in response.categories_analysis
                if item.category == TextCategory.SEXUAL
            )
            violence_result = next(
                item
                for item in response.categories_analysis
                if item.category == TextCategory.VIOLENCE
            )

            res = {
                "Hate": hate_result.severity,
                "SelfHarm": self_harm_result.severity,
                "Adult": sexual_result.severity,
                "Violence": violence_result.severity,
            }
            return res
