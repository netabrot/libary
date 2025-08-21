from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SQLALCHEMY_DATABASE_URL: str = 'sqlite:///./library.db'

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()