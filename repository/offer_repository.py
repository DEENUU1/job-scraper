from typing import List
from sqlalchemy.orm import Session
from models.offer import Offer as OfferModel
from schemas.offer import Offer, OfferOutput
from enums.sort_by import OfferSortEnum
from sqlalchemy import asc, desc


class OfferRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Offer, website: str) -> None:
        db_offer = OfferModel(
            title=data.title,
            url=data.url,
            page=website,
            check=False
        )
        self.session.add(db_offer)
        self.session.commit()
        self.session.refresh(db_offer)
        return

    def offer_exists_by_url(self, url: str) -> bool:
        return self.session.query(OfferModel).filter(OfferModel.url == url).first() is not None

    def offer_exists_by_id(self, _id: int) -> bool:
        return self.session.query(OfferModel).filter(OfferModel.id == _id).first() is not None

    def change_check_status(self, _id: int, status: bool) -> bool:
        db_offer = self.session.query(OfferModel).filter(OfferModel.id == _id).first()
        db_offer.check = status
        self.session.commit()
        self.session.refresh(db_offer)
        return True

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50,
            query: str = None,
            checked: bool = None,
            unchecked: bool = None,
            sort_by: OfferSortEnum = OfferSortEnum.NEWEST
    ) -> List[OfferOutput]:
        offers = self.session.query(OfferModel)

        if query is not None:
            offers = offers.filter(OfferModel.title.like(f'%{query}%'))

        if checked is not None:
            offers = offers.filter(OfferModel.check == checked)

        if unchecked is not None:
            offers = offers.filter(OfferModel.check == unchecked)

        if sort_by == OfferSortEnum.NEWEST:
            offers = offers.order_by(desc(OfferModel.created_at))
        elif sort_by == OfferSortEnum.OLDEST:
            offers = offers.order_by(asc(OfferModel.created_at))

        offset = (page - 1) * page_limit if page > 0 else 0
        offers = offers.offset(offset).limit(page_limit).all()

        return [OfferOutput(**offer.__dict__) for offer in offers]
