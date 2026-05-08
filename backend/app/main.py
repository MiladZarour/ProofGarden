from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers import evidence, investigations, reports, uploads
from app.schemas import HealthResponse
from app.utils.files import UPLOAD_DIR, ensure_upload_dir


def cors_origins() -> list[str]:
    configured = os.getenv("PROOFGARDEN_CORS_ORIGINS")
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        f"http://localhost:{port}" for port in range(5173, 5180)
    ] + [
        f"http://127.0.0.1:{port}" for port in range(5173, 5180)
    ]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    ensure_upload_dir()
    init_db()
    yield


app = FastAPI(
    title="ProofGarden API",
    description="Open-source evidence workspace API for structured verification investigations.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


app.include_router(investigations.router, prefix="/api")
app.include_router(uploads.router, prefix="/api")
app.include_router(evidence.router, prefix="/api")
app.include_router(reports.router, prefix="/api")

ensure_upload_dir()
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
