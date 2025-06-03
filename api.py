import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

# Add the current directory to the path so we can import the sentiment module
sys.path.append(os.path.join(os.path.dirname(__file__), "agents"))

# Import the sentiment analysis tools
from agents.sentiment import Sentimental_tool
from textblob import TextBlob

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="MindMesh API")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Define request models
class SentimentRequest(BaseModel):
    text: str
    user: Optional[str] = "Anonymous"
    days: Optional[str] = "recent"

class SentimentResponse(BaseModel):
    polarity: float
    subjectivity: float
    sentiment: str
    analysis: str
    advice: str

# Initialize the sentiment tool
sentiment_tool = Sentimental_tool()

# Function to run sentiment analysis in a separate thread
def analyze_sentiment(text: str) -> Dict[str, float]:
    return sentiment_tool._run(text)

# Function to get sentiment label based on polarity
def get_sentiment_label(polarity: float) -> str:
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

# Function to generate advice based on sentiment
def generate_advice(sentiment: str, polarity: float, subjectivity: float) -> str:
    if sentiment == "positive":
        return "Your emotions appear to be positive. Continue with activities that bring you joy and maintain this positive mindset."
    elif sentiment == "negative":
        if polarity < -0.5:
            return "Your emotions appear to be strongly negative. It might be beneficial to speak with a mental health professional for support and guidance."
        else:
            return "Your emotions appear to be somewhat negative. Consider practicing mindfulness, engaging in physical activity, or talking to someone you trust about your feelings."
    else:
        return "Your emotions appear to be neutral. This is a good time for self-reflection and setting new goals for your mental well-being."

# Function to generate analysis based on sentiment
def generate_analysis(sentiment: str, polarity: float, subjectivity: float) -> str:
    intensity = abs(polarity)
    if sentiment == "positive":
        if intensity > 0.7:
            analysis = "Your text shows very strong positive emotions."
        elif intensity > 0.4:
            analysis = "Your text shows moderately positive emotions."
        else:
            analysis = "Your text shows slightly positive emotions."
    elif sentiment == "negative":
        if intensity > 0.7:
            analysis = "Your text shows very strong negative emotions."
        elif intensity > 0.4:
            analysis = "Your text shows moderately negative emotions."
        else:
            analysis = "Your text shows slightly negative emotions."
    else:
        analysis = "Your text shows neutral emotions."
    
    if subjectivity > 0.7:
        analysis += " Your text is highly subjective, indicating strong personal opinions or feelings."
    elif subjectivity > 0.4:
        analysis += " Your text is moderately subjective, showing some personal opinions or feelings."
    else:
        analysis += " Your text is relatively objective, focusing more on facts than feelings."
    
    return analysis

@app.get("/")
async def root():
    return {"message": "Welcome to MindMesh API"}

@app.post("/analyze", response_model=SentimentResponse)
async def analyze(request: SentimentRequest):
    try:
        logger.info(f"Analyzing sentiment for user: {request.user}")
        
        # Run sentiment analysis in a separate thread to avoid blocking
        with ThreadPoolExecutor() as executor:
            sentiment_result = await asyncio.get_event_loop().run_in_executor(
                executor, analyze_sentiment, request.text
            )
        
        polarity = sentiment_result["polarity"]
        subjectivity = sentiment_result["subjectivity"]
        sentiment = get_sentiment_label(polarity)
        
        analysis = generate_analysis(sentiment, polarity, subjectivity)
        advice = generate_advice(sentiment, polarity, subjectivity)
        
        logger.info(f"Sentiment analysis completed: {sentiment}")
        
        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment": sentiment,
            "analysis": analysis,
            "advice": advice
        }
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=12000, reload=True)