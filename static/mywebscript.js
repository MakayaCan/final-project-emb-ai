"use strict";

function RunSentimentAnalysis() {
    const textToAnalyze = document
        .getElementById("textToAnalyze")
        .value
        .trim();

    const output = document.getElementById("system_response");

    if (!textToAnalyze) {
        output.textContent = "Invalid text! Please try again!";
        return;
    }

    output.textContent = "Analyzing...";

    fetch(
        `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`
    )
        .then(async (response) => {
            const message = await response.text();

            if (!response.ok) {
                throw new Error(message);
            }

            return message;
        })
        .then((message) => {
            output.textContent = message;
        })
        .catch((error) => {
            output.textContent = error.message;
        });
}
