import logging
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from pathlib import Path
from dotenv import load_dotenv
from config.config import Config

logger = logging.getLogger(__name__)

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)


class ContentChecker:
    def __init__(self):
        self.endpoint = os.getenv("AI_ENDPOINT")
        self.key = AzureKeyCredential(os.getenv("AI_KEY"))

    def analyze_text(self, text):
        text = text[:10000]
        client = ContentSafetyClient(self.endpoint, self.key)
        request = AnalyzeTextOptions(text=text)
        try:
            response = client.analyze_text(request)
        except Exception:
            print(Config.ANALYSE_TEXT_FAILED)
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
