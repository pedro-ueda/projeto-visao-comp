import os
from pathlib import Path

class Config:
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", 
        "postgresql+psycopg://postgres:postgres@localhost:5432/vision_db"
    )
    UPLOAD_FOLDER: Path = Path(os.environ.get("UPLOAD_FOLDER", "assets/images"))
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "super-secret-dev-key")

    @classmethod
    def init_app(cls):
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)