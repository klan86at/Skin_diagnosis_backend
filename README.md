# Skin_diagnosis_backend

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

## Overview

The `skin_diagnosis_backend` is a RESTful API built with FastAPI to analyze skin conditions using user-uploaded images and text descriptions. It integrates with the Groq API to deliver AI-driven diagnoses, including detailed observations, explanations, and recommendations. This backend supports a front-end application hosted at `https://skin-condition-diagnosis-rag.vercel.app`, enabling users to upload images and receive actionable insights.

## Features

- **Image and Text Processing**: Handles image uploads and text descriptions via the `POST /analyze/` endpoint.
- **AI Integration**: Utilizes the Groq API for advanced skin condition analysis.
- **CORS Support**: Configured to allow requests from the front-end (`https://skin-condition-diagnosis-rag.vercel.app`).
- **Logging**: Comprehensive logging for debugging and monitoring.
- **Environment Management**: Uses `.env` for secure API key configuration.

## Tech Stack

- **Framework**: FastAPI 0.115.12
- **Language**: Python 3.9+
- **Dependencies**: `requests`, `python-dotenv`, `python-multipart`, `uvicorn`
- **Hosting**: Deployed on Render
- **API Integration**: Groq API for AI-driven analysis

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git
- A Groq API key (obtain from [Groq](https://groq.com))

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/****-username/skin_diagnosis_backend.git
