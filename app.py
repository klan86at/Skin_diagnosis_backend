# File: app.py
import os
import requests
import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load Groq API key from environment variables (set in Render)
groq_api_key = os.getenv("groq_api_key")
logger.info(f"Groq API key found: {bool(groq_api_key)}")  # Added for debugging
if not groq_api_key:
    logger.error("Groq API key not found.")
    raise ValueError("Groq API key not found. Please set it in your environment variables.")

# FastAPI app setup
app = FastAPI()

# Enable CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vercel.com/ken-langats-projects/skin-condition-diagnosis-rag"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rest of your code...
