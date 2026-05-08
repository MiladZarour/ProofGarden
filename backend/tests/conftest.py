import os
import shutil
from pathlib import Path

os.environ.setdefault("PROOFGARDEN_DATABASE_URL", "sqlite:///./test_proofgarden.db")
os.environ.setdefault("PROOFGARDEN_UPLOAD_DIR", "./test_uploads")

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    upload_dir = Path(os.environ["PROOFGARDEN_UPLOAD_DIR"])
    if upload_dir.exists():
        shutil.rmtree(upload_dir)


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def investigation_payload() -> dict:
    return {
        "title": "Suspicious delivery text",
        "claim": "A courier claims the recipient must pay a fee before delivery.",
        "category": "Scam message",
        "source_url": None,
        "description": "Message received by SMS with a shortened link.",
        "status": "Unverified",
    }

