from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CryptoInsight"
    app_env: str = "development"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    rate_limit_per_minute: int = 60

    coingecko_api_key: str = ""
    coingecko_base_url: str = "https://api.coingecko.com/api/v3"

    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
