import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env

class Settings:
    DB_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///./app/db/database.db")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "SUPER_SECRET_KEY_:D")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256") # Алгоритм, который будет использоваться для шифрования JWT-токенов
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")) # Время жизни токена в минутах

settings = Settings()
