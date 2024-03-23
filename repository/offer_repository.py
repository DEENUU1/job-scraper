from typing import List, Type, Optional
from pydantic import UUID4
from sqlalchemy.orm import Session
from models.offer import Offer
from schemas.offer_schema import OfferInput, OfferOutput
from enums.sort import SortEnum
from enums.status import StatusEnum
from sqlalchemy import asc, desc


class OfferRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, offer_input: OfferInput, website_id: UUID4) -> OfferOutput:
        offer = Offer(**offer_input.model_dump(exclude_none=True), website_id=website_id)
        self.session.add(offer)
        self.session.commit()
        self.session.refresh(offer)
        return OfferOutput(**offer.__dict__)

    def offer_exists_by_url(self, url: str) -> bool:
        offer = self.session.query(Offer).filter_by(url=url).first()
        return bool(offer)

    def offer_exists_by_id(self, offer_id: UUID4) -> bool:
        offer = self.session.query(Offer).filter_by(id=offer_id).first()
        return bool(offer)

    def get_offer_object_by_url(self, url: str) -> Type[Offer]:
        return self.session.query(Offer).filter_by(url=url).first()

    def get_offer_object_by_id(self, offer_id: UUID4) -> Type[Offer]:
        return self.session.query(Offer).filter_by(id=offer_id).first()

    def get_offer_by_id(self, offer_id: UUID4) -> Type[Offer]:
        return self.session.query(Offer).filter_by(id=offer_id).first()

    def get_offers_by_website_id(
            self,
            website_id: UUID4,
            sort: SortEnum = SortEnum.NEWEST,
            archived: bool = False,
            query: Optional[str] = None,
            status: Optional[StatusEnum] = None,
    ) -> List[OfferOutput]:

        offers = self.session.query(Offer)

        offers = offers.filter(Offer.website_id == website_id).filter(Offer.archived == archived)

        if sort == SortEnum.OLDEST:
            offers = offers.order_by(asc(Offer.created_at))
        elif sort == SortEnum.NEWEST:
            offers = offers.order_by(desc(Offer.created_at))

        if query:
            offers = offers.filter(Offer.title.ilike(f'%{query}%'))

        if status:
            offers = offers.filter(Offer.status == status)

        return [OfferOutput(**offer.__dict__) for offer in offers.all()]

    def update_archive(self, offer: Type[Offer]) -> OfferOutput:
        offer.archived = not offer.archived
        self.session.commit()
        self.session.refresh(offer)
        return OfferOutput(**offer.__dict__)

    def update_status(self, offer: Type[Offer], status: StatusEnum) -> OfferOutput:
        offer.status = status
        self.session.commit()
        self.session.refresh(offer)
        return OfferOutput(**offer.__dict__)
