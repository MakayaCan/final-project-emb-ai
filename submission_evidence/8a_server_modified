"""Flask application for IBM Watson emotion detection."""

import requests

from flask import Flask, jsonify, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Display the emotion detection interface."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    """Analyze text and return its emotion scores."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    if not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    try:
        result = emotion_detector(text_to_analyze)
    except requests.exceptions.RequestException:
        app.logger.exception("Watson service request failed")
        return "Emotion detection service is unavailable.", 502
    except (KeyError, IndexError, TypeError, ValueError):
        app.logger.exception("Unexpected Watson response")
        return "Unable to process the supplied text.", 502

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    summary = (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return summary, 200


@app.route("/health", methods=["GET"])
def health():
    """Return application health status."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
