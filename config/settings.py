from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    title: str = "JobScraper"


settings = Settings()
