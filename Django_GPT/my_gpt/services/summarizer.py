from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device


MODEL_NAME = "sshleifer/distilbart-cnn-6-6"


@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        device=get_pipeline_device(),
    )


def summarize_text(text):
    summarizer = get_summarizer_pipeline()

    result = summarizer(
        text,
        max_length=150,
        min_length=30,
        do_sample=False,
        truncation=True,
    )

    summary = result[0]["summary_text"]

    original_length = len(text)
    summary_length = len(summary)

    compression_ratio = round(
        (1 - summary_length / original_length) * 100,
        2,
    )

    return {
        "summary": summary,
        "original_length": original_length,
        "summary_length": summary_length,
        "compression_ratio": compression_ratio,
    }