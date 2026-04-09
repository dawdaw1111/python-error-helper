import os


class Settings:
    admin_username = os.getenv("PYERR_ADMIN_USERNAME", "admin")
    admin_password = os.getenv("PYERR_ADMIN_PASSWORD", "admin123456")
    token_secret = os.getenv("PYERR_TOKEN_SECRET", "pyerr-dev-secret")
    token_expire_seconds = int(os.getenv("PYERR_TOKEN_EXPIRE_SECONDS", "86400"))
    database_url = os.getenv("PYERR_DATABASE_URL", "sqlite:///./pyerr.db")
    cors_origins = [
        item.strip()
        for item in os.getenv(
            "PYERR_CORS_ORIGINS",
            "http://127.0.0.1:5173,http://127.0.0.1:5174,http://localhost:5173,http://localhost:5174",
        ).split(",")
        if item.strip()
    ]


settings = Settings()
