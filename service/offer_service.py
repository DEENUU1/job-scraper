from typing import List

from sqlalchemy.orm import Session

from enums.sort_by import OfferSortEnum
from repository.offer_repository import OfferRepository
from schemas.offer import Offer, OfferOutput


class OfferService:
    def __init__(self, session: Session):
        self.repository = OfferRepository(session)

    def create(self, data: Offer, website: str) -> None:
        if self.repository.offer_exists_by_url(data.url):
            print("Offer exists in database")
            return

        self.repository.create(data, website)
        print("Offer created")

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50,
            query: str = None,
            checked: bool = None,
            unchecked: bool = None,
            sort_by: OfferSortEnum = OfferSortEnum.NEWEST
    ) -> List[OfferOutput]:
        return self.repository.get_all(
            page,
            page_limit,
            query,
            checked,
            unchecked,
            sort_by
        )

    def change_check_status(self, _id: int, status: bool) -> bool:
        return self.repository.change_check_status(_id, status)
