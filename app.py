# File: app.py
# Libraries
import os
import requests
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load Groq API key from .env
load_dotenv()
groq_api_key = os.getenv("groq_api_key")
if not groq_api_key:
    logger.error("Groq API key not found.")
    raise ValueError("Groq API key not found. Please set it in your .env file.")

# FastAPI app setup
app = FastAPI()

# Enable CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vercel.com/ken-langats-projects/skin-condition-diagnosis-rag"],  # Restrict this to your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core function to analyze skin condition using Groq
def analyze_skin_condition(query: str, description: str) -> dict:
    try:
        combined_text = f"{query} The image shows: {description}"

        payload = {
            "model": "deepseek-r1-distill-llama-70b",  # Replace with your desired model "qwen-qwq-32b"
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
@app.post("/analyze/")
async def analyze_endpoint(
    image: UploadFile = File(...),
    description: str = Form(...)
):
    logger.info(f"Received request with description: {description}")
    logger.info(f"Uploaded image filename: {image.filename}")

    temp_image_path = None  # Initialize temp_image_path to avoid reference errors
    try:
        # Save image temporarily (optional)
        image_bytes = await image.read()
        temp_image_path = f"temp_{image.filename}"
        with open(temp_image_path, "wb") as f:
            f.write(image_bytes)

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
            return {"error": api_response.get("error", "No response from model.")}

    finally:
        # Ensure cleanup happens even if an error occurs
        if temp_image_path and os.path.exists(temp_image_path):
            logger.info(f"Cleaning up temporary file: {temp_image_path}")
            os.remove(temp_image_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

# To run this: uvicorn app:app --reload
