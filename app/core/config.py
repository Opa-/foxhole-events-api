from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    CELERY_BROKER_URL: str = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://127.0.0.1:6379/0"
    CACHE_REDIS_HOST: str = "127.0.0.1"
    CACHE_REDIS_PORT: int = 6379
    CACHE_REDIS_DB: int = 1
    DATABASE_URL: str = "postgresql://opa@127.0.0.1/foxhole"
    UVICORN_RELOAD: bool = True
    API_INTERNAL_URL: str = "http://localhost:8000"


settings = Settings()
