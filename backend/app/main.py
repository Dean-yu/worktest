from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(title="AI Conversation Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def home() -> dict:
    return {"message": "Open /frontend/index.html"}
