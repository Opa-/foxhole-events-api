from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    celery_broker_url: str = "redis://127.0.0.1:6379/0"
    celery_result_backend: str = "redis://127.0.0.1:6379/0"
    cache_redis_host: str = "127.0.0.1"
    cache_redis_port: int = 6379
    cache_redis_db: int = 1
    database_url: str = "postgresql://postgres@127.0.0.1/foxhole"


settings = Settings()
