from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device


MODEL_NAME = "unitary/toxic-bert"


@lru_cache(maxsize=1)
def get_moderator_pipeline():
    return pipeline(
        task="text-classification",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        device=get_pipeline_device(),
    )


def analyze_toxicity(text):
    moderator = get_moderator_pipeline()

    results = moderator(
        text,
        top_k=None,
        truncation=True,
    )

    labels = []

    for item in results:
        labels.append({
            "label": item["label"],
            "score": round(item["score"] * 100, 2),
        })

    highest = max(labels, key=lambda x: x["score"])

    return {
        "top_label": highest["label"],
        "top_score": highest["score"],
        "labels": labels,
    }