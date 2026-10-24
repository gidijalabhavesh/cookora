import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAIError
from pydantic import BaseModel, ConfigDict, Field
from starlette.concurrency import run_in_threadpool

from model import generate_recipe
from tools import parse_ingredients, validate_recipe_request


logger = logging.getLogger(__name__)
frontend_url = os.getenv("FRONTEND_URL", "")
allowed_origins = [
    origin.strip()
    for origin in frontend_url.split(",")
    if origin.strip()
]
allowed_origins.extend(
    [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
)

app = FastAPI(title="Smart Recipe Generator API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(dict.fromkeys(allowed_origins)),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class RecipeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    ingredients: str = Field(min_length=1, max_length=2000)
    cuisine: str = Field(default="Any", min_length=1, max_length=50)
    servings: int = Field(default=2, ge=1, le=12)
    diet: str = Field(default="No preference", min_length=1, max_length=50)
    extra: str = Field(default="", max_length=500)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "aiConfigured": bool(os.getenv("OPENAI_API_KEY")),
    }


@app.post("/api/recipes")
async def create_recipe(request: RecipeRequest):
    ingredients = parse_ingredients(request.ingredients)
    try:
        validate_recipe_request(ingredients, request.servings)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    try:
        recipe = await run_in_threadpool(
            generate_recipe,
            ingredients,
            request.cuisine,
            request.servings,
            request.diet,
            request.extra,
        )
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except OpenAIError as error:
        logger.exception("Recipe generation failed because of the AI provider.")
        raise HTTPException(
            status_code=502,
            detail="The recipe service could not complete the request. Please try again.",
        ) from error

    return {"recipe": recipe}


frontend_path = Path(__file__).resolve().parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
