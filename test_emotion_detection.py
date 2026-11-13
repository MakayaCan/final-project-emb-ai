"""Unit tests for the emotion detection application."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class EmotionDetectionTests(unittest.TestCase):
    """Test the Watson emotion detection function."""

    def setUp(self):
        self.emotions = {
            "anger": 0.10,
            "disgust": 0.05,
            "fear": 0.15,
            "joy": 0.60,
            "sadness": 0.10
        }

    @patch("emotion_detection.requests.post")
    def test_dominant_emotion_is_joy(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [
                {"emotion": self.emotions}
            ]
        }
        mock_post.return_value = response

        result = emotion_detector("I am very happy")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.60)

    @patch("emotion_detection.requests.post")
    def test_dominant_emotion_is_anger(self, mock_post):
        emotions = dict(self.emotions)
        emotions["anger"] = 0.80

        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [
                {"emotion": emotions}
            ]
        }
        mock_post.return_value = response

        result = emotion_detector("I am very angry")

        self.assertEqual(result["dominant_emotion"], "anger")

    @patch("emotion_detection.requests.post")
    def test_dominant_emotion_is_sadness(self, mock_post):
        emotions = dict(self.emotions)
        emotions["sadness"] = 0.90

        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [
                {"emotion": emotions}
            ]
        }
        mock_post.return_value = response

        result = emotion_detector("I feel sad")

        self.assertEqual(result["dominant_emotion"], "sadness")

    @patch("emotion_detection.requests.post")
    def test_http_400_returns_none_values(self, mock_post):
        response = Mock()
        response.status_code = 400
        mock_post.return_value = response

        result = emotion_detector("invalid request")

        for key in ("anger", "disgust", "fear", "joy", "sadness"):
            self.assertIsNone(result[key])

        self.assertIsNone(result["dominant_emotion"])

    def test_blank_input_does_not_call_service(self):
        with patch("emotion_detection.requests.post") as mock_post:
            result = emotion_detector("   ")

        mock_post.assert_not_called()
        self.assertIsNone(result["dominant_emotion"])

    @patch("emotion_detection.requests.post")
    def test_all_five_emotions_are_returned(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [
                {"emotion": self.emotions}
            ]
        }
        mock_post.return_value = response

        result = emotion_detector("Test sentence")

        expected_keys = {
            "anger", "disgust", "fear", "joy",
            "sadness", "dominant_emotion"
        }

        self.assertEqual(set(result.keys()), expected_keys)


if __name__ == "__main__":
    unittest.main()
