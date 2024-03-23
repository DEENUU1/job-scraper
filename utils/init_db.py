from config.database import engine
from models.offer import Offer
from models.website import Website


def init_db() -> None:
    Website.metadata.create_all(bind=engine)
    Offer.metadata.create_all(bind=engine)
