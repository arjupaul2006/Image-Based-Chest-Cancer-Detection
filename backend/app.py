from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from io import BytesIO
from PIL import Image
import numpy as np
import uvicorn

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.chest_cancer_classification.pipeline.prediction import PredictionPipeline
load_dotenv()

FRONTEND_URL = os.getenv('FRONTEND_URL')
if not FRONTEND_URL:
    raise ValueError("FRONTEND_URL is not set in the environment variables.")

# --------------------------------------------------
# Lifespan
# --------------------------------------------------

from contextlib import asynccontextmanager
from fastapi import FastAPI
from huggingface_hub import hf_hub_download
from tensorflow.keras.models import load_model


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting Chest Cancer Detection API...")

    # Download model from Hugging Face
    model_path = hf_hub_download(
        repo_id="arjupaul/chest-cancer-classification",
        filename="model_v3.keras"
    )

    # Load model
    app.state.model = load_model(
        model_path,
        safe_mode=False
    )

    print("Chest cancer model loaded successfully.")
    print("FastAPI is ready.")

    yield

    print("Shutting down Chest Cancer Detection API...")



# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="Chest Cancer Detection",
    lifespan=lifespan
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        # Add your deployed frontend URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Chest Cancer Detection API is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        file_byte = await file.read()
        image = Image.open(BytesIO(file_byte)).convert('RGB')

        # Create a prediction pipeline
        pipeline = PredictionPipeline(model=app.state.model, image=image)

        # Make prediction
        predicted_class, confidence = pipeline.predict()

        return {
            "predicted_class": predicted_class,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
