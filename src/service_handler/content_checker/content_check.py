from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
import src.keys
import logging
from config.log_config.log_config import LogStatements
logger = logging.getLogger('content_checker')


class ContentChecker:
    def __init__(self):
        self.endpoint = "https://youtube-transcript-summariser.cognitiveservices.azure.com/"
        self.key = AzureKeyCredential("c702ec3b4b194de3a22d767b6bec6001")

    def analyze_text(self, text):
        text = text[:10000]
        client = ContentSafetyClient(self.endpoint, self.key) 
        request = AnalyzeTextOptions(text=text)
        try:
            response = client.analyze_text(request)
        except Exception:
            print("Analyze text failed.")
            return False
        else:
            if response.hate_result:
                res = {
                        "Hate": response.hate_result.severity,
                        "SelfHarm": response.self_harm_result.severity,
                        "Adult": response.sexual_result.severity,
                        "Violence": response.violence_result.severity
                       }
                return res
