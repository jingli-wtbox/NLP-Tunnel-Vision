import os
from fastapi import FastAPI, HTTPException, status
from openai import OpenAI
from contextlib import asynccontextmanager
from utils import (
    RequestBody,
    OpenAIAPIKeyError,
    OpenAPIError
)
from inference import infer

openai_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if os.getenv('OPENAI_API_KEY', None) is None:
            raise OpenAIAPIKeyError("OPENAI_API_KEY is not set.")
        global openai_client
        openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        yield
        print("Closing OpenAI client...")
        if openai_client is not None:
            del openai_client
    except Exception as e:
        raise OpenAPIError(str(e))


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"project": "NLP Tunnel Vision @ AUT 2024"}

@app.get("/about")
async def about():
    project_details = {
        "project": "NLP Tunnel Vision",
        "description": "A project to fine-tune GPT-3.5 for NLP tunnel vision.",
        "fine_tuned_model_id": os.getenv("OPENAI_FINE_TUNED_MODEL_ID", None),
    }
    return project_details


@app.post("/infer", status_code = status.HTTP_200_OK)
async def openai_infer(request_body: RequestBody):
    try:
        if openai_client is None:
            raise OpenAPIError("OpenAI client is not initialized.")
        response = infer(openai_client, request_body)        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))