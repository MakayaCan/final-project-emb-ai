"""Emotion detection using the IBM Watson NLP service."""

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)

HEADERS = {
    "grpc-metadata-mm-model-id":
        "emotion_aggregated-workflow_lang_en_stock"
}

EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return the five emotion scores and the dominant emotion."""
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return {
            **dict.fromkeys(EMOTION_KEYS),
            "dominant_emotion": None
        }

    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    response = requests.post(
        URL,
        json=payload,
        headers=HEADERS,
        timeout=45
    )

    if response.status_code == 400:
        return {
            **dict.fromkeys(EMOTION_KEYS),
            "dominant_emotion": None
        }

    response.raise_for_status()

    result = response.json()
    emotions = result["emotionPredictions"][0]["emotion"]

    scores = {
        key: emotions[key]
        for key in EMOTION_KEYS
    }

    scores["dominant_emotion"] = max(
        EMOTION_KEYS,
        key=scores.get
    )

    return scores
