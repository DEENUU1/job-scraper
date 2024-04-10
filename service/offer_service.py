from repository.offer_repository import OfferRepository
from sqlalchemy.orm import Session
from schemas.offer import Offer


class OfferService:
    def __init__(self, session: Session):
        self.repository = OfferRepository(session)

    def create(self, data: Offer) -> bool:
        if self.repository.offer_exists_by_url(data.url):
            return False

        return self.repository.create(data)
