import logging
from config.log_config.log_config import LogStatements

logger = logging.getLogger(__name__)


def save_summary(self, summary, hid):
    with open(
        f"src/downloadable_results/summary_outputs/{hid}_summary.txt",
        "w",
        encoding="utf-8",
    ) as f:
        lines = summary.split(".")
        f.writelines(lines)
    logger.info(LogStatements.summary_generated)
    print(f"Summary File Generated with id - {hid}")


def save_transcript(self, transcript, hid):
    with open(
        f"src/downloadable_results/transcript_outputs/{hid}_transcript.txt",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(transcript)
    logger.info(LogStatements.transcript_generated)
    print(f"Transcript File Generated with id - {hid}")


def show_video_details(self, transcript, summary, hid):
    read_transcript = transcript
    read_summary = summary
    transcript_word = read_transcript.split()
    summary_word = read_summary.split()
    print(
        f"Video URLID - {hid}\nTranscript Length - {len(transcript_word)}\nSummary Length - {len(summary_word)}"
    )
