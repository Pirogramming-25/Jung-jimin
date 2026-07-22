from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device


MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    """
    감정 분석 모델을 최초 요청 시 한 번만 불러옵니다.
    이후 요청에서는 캐시된 모델을 재사용합니다.
    """

    return pipeline(
        task="sentiment-analysis",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        device=get_pipeline_device(),
    )


def analyze_sentiment(text):
    """입력 문장의 감정과 신뢰도를 반환합니다."""

    sentiment_pipeline = get_sentiment_pipeline()
    result = sentiment_pipeline(text, truncation=True)[0]

    label = result["label"].lower()
    score = round(result["score"] * 100, 2)

    label_names = {
        "positive": "긍정",
        "neutral": "중립",
        "negative": "부정",
    }

    return {
        "label": label,
        "label_ko": label_names.get(label, label),
        "score": score,
    }