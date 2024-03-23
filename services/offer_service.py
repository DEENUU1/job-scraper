from enums.sort import SortEnum
from enums.status import StatusEnum
from repository.offer_repository import OfferRepository
from sqlalchemy.orm import Session
from schemas.offer_schema import OfferInput, OfferOutput
from pydantic import UUID4
from repository.website_repository import WebsiteRepository
from typing import List, Optional


class OfferService:
    def __init__(self, session: Session) -> None:
        self.offer_repository = OfferRepository(session)
        self.website_repository = WebsiteRepository(session)

    def create(self, offer_input: OfferInput, website_id: UUID4) -> Optional[OfferOutput]:
        if self.offer_repository.offer_exists_by_url(offer_input.url):
            return

        if not self.website_repository.website_exists_by_id(website_id):
            return

        return self.offer_repository.create(offer_input, website_id)

    def get_offers(
            self,
            sort: SortEnum = SortEnum.NEWEST,
            website_id: Optional[UUID4] = None,
            archived: bool = False,
            query: Optional[str] = None,
            status: Optional[StatusEnum] = None
    ) -> List[OfferOutput]:
        return self.offer_repository.get_offers_by_website_id(
            sort,
            website_id,
            archived,
            query,
            status
        )

    def update_archive(self, offer_id: UUID4) -> Optional[OfferOutput]:
        if not self.offer_repository.offer_exists_by_id(offer_id):
            return

        offer = self.offer_repository.get_offer_object_by_id(offer_id)

        return self.offer_repository.update_archive(offer)

    def update_status(self, offer_id: UUID4, status: StatusEnum) -> Optional[OfferOutput]:
        if not self.offer_repository.offer_exists_by_id(offer_id):
            return

        offer = self.offer_repository.get_offer_object_by_id(offer_id)

        return self.offer_repository.update_status(offer, status)
