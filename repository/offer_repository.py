from typing import List, Type
from sqlalchemy.orm import Session
from models.offer import Offer as OfferModel
from schemas.offer import Offer, OfferOutput


class OfferRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Offer) -> bool:
        db_offer = OfferModel(**data.model_dump(exclude_none=True))
        self.session.add(db_offer)
        self.session.commit()
        self.session.refresh(db_offer)
        return True

    def offer_exists_by_url(self, url: str) -> bool:
        return self.session.query(OfferModel).filter(OfferModel.url == url).first() is not None

    def change_check_status(self, _id: int, status: bool) -> bool:
        db_offer = self.session.query(OfferModel).filter(OfferModel.id == _id).first()
        if db_offer is None:
            return False
        db_offer.checked = status
        self.session.commit()
        return True

