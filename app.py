import os
import requests
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("groq_api_key")
if not groq_api_key:
    logger.error("GROQ_API_KEY not found.")
    raise ValueError("GROQ_API_KEY not found. Please set it in your .env file or Render environment variables.")

# FastAPI app setup
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://skin-condition-diagnosis-rag.vercel.app",
        "http://localhost:3000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}

# Core function to analyze skin condition using Groq
def analyze_skin_condition(query: str, description: str) -> dict:
    try:
        combined_text = f"{query} The image shows: {description}"

        payload = {
            "model": "deepseek-r1-distill-llama-70b",
            "messages": [{"role": "user", "content": combined_text}],
            "max_tokens": 2000,
            "temperature": 0.3
        }

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        logger.info("Sending request to Groq API")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP Error {e.response.status_code}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": str(e)}

# API Endpoint
@app.post("/analyze")
async def analyze_endpoint(
    image: UploadFile = File(...),
    description: str = Form(...)
):
    logger.info(f"Received request with description: {description}")
    logger.info(f"Uploaded image filename: {image.filename}")

    try:
        # Read image bytes directly without saving to disk
        image_bytes = await image.read()

        query = (
            "Provide a detailed analysis of this skin condition. "
            "Structure the response with key observations, explanations, and final recommendations."
        )

        logger.info("Sending request to Groq API")
        api_response = analyze_skin_condition(query, description)

        if api_response and "choices" in api_response:
            logger.info("Successfully received response from Groq API")
            return {"diagnosis": api_response["choices"][0]["message"]["content"]}
        else:
            logger.error("Error in Groq API response")
            raise HTTPException(status_code=500, detail=api_response.get("error", "No response from model."))

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
