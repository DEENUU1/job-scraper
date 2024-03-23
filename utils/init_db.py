from config.database import engine
from models.website import Website


def init_db() -> None:
    Website.metadata.create_all(bind=engine)
