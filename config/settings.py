from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TITLE: str = "JobScraper"


settings = Settings()
