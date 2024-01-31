import oneai

# import keys
import logging

# import torch
from transformers import pipeline
from config.config import Config

logger = logging.getLogger(__name__)


class SummaryGenerator:
    # def __init__(self):
    # set a One AI API key, following API calls will use this key
    # oneai.api_key = keys.oneai_api_key

    # def summary_generator(self, your_input):
    #     # define a pipeline for processing str inputs
    #     try:
    #         size = len(your_input)
    #         pipeline = oneai.Pipeline(steps=[oneai.skills.Summarize(min_length=size/4, max_length=size/3),])
    #         # process the input and store the output
    #         output = pipeline.run(your_input)
    #         # print the summary
    #         summary = output.summary.text
    #         return summary
    #     except Exception:
    #         print("Summary Generation Failed. Try Again!")
    #         return None

    def summary_generator(self, your_input):
        # define a pipeline for processing str inputs
        try:
            if your_input is not None:
                size = len(your_input)
                # summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                # # process the input and store the output
                # # print the summary
                # summary = summarizer(your_input, max_length=size/3, min_length=size/4, do_sample=False)
                summary = your_input[:200]
                return summary
            return None
        except Exception:
            print(Config.SUMMARY_GENERATION_FAILED)
