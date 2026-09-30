import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "jpg",
        "jpeg",
        "jpe",
        "png",
        "webp"
    }

    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = "crop_disease_db"