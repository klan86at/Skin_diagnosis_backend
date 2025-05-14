# File: api_backend.py
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
    allow_origins=["https://vercel.com/ken-langats-projects/skin-condition-diagnosis-rag"],  # For production, restrict this to your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core function to analyze skin condition using Groq
def analyze_skin_condition(query: str, description: str) -> dict:
    try:
        combined_text = f"{query} The image shows: {description}"

        payload = {
            "model": "deepseek-r1-distill-llama-70b", #"qwen-qwq-32b",
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
    # Save image temporarily (optional)
    image_bytes = await image.read()
    temp_image_path = f"temp_{image.filename}"
    with open(temp_image_path, "wb") as f:
        f.write(image_bytes)

    query = (
        "Provide a detailed analysis of this skin condition. "
        "Structure the response with key observations, explanations, and final recommendations."
    )

    api_response = analyze_skin_condition(query, description)

    # Clean up temp image
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

    if api_response and "choices" in api_response:
        return {"diagnosis": api_response["choices"][0]["message"]["content"]}
    else:
        return {"error": api_response.get("error", "No response from model.")}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_test:app", host="127.0.0.1", port=8000, reload=True)


# To run this: uvicorn api_backend:app --reload