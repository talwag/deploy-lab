import re

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "awesome", "fantastic",
    "wonderful", "love", "loved", "like", "liked", "happy", "best",
    "nice", "perfect", "positive", "beautiful", "enjoy", "enjoyed",
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "horrible", "hate", "hated", "worst",
    "poor", "disappointing", "disappointed", "sad", "angry", "negative",
    "broken", "fail", "failed", "problem", "issue", "annoying",
}


class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    sentiment: str
    text: str
    version: str


def classify_sentiment(text: str) -> str:
    words = re.findall(r"[a-zA-Z']+", text.lower())
    positive_count = sum(1 for word in words if word in POSITIVE_WORDS)
    negative_count = sum(1 for word in words if word in NEGATIVE_WORDS)

    if positive_count > negative_count:
        return "positive"
    if negative_count > positive_count:
        return "negative"
    return "neutral"


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    sentiment = classify_sentiment(request.text)
    return AnalyzeResponse(sentiment=sentiment, text=request.text, version="4.0")
