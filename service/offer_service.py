from typing import Optional, List

from sqlalchemy.orm import Session

from enums.sort_by import OfferSortEnum
from repository.offer_repository import OfferRepository
from schemas.offer import Offer, OfferListOutput

from fastapi import HTTPException

from schemas.tag import TagOutput


class OfferService:
    def __init__(self, session: Session):
        """
        Initializes the OfferService with a database session.

        Args:
            session (sqlalchemy.orm.Session): The database session to use for operations.
        """
        self.repository = OfferRepository(session)

    def create(self, data: Offer, website: str, tag: Optional[str]) -> None:
        """
        Creates a new offer in the database, checking for duplicates first.

        Args:
            data (Offer): The offer data to be saved.
            website (str): The website where the offer was found.

        Returns:
            None
        """
        if self.repository.offer_exists_by_url(data.url):
            print("Offer exists in database")
            return

        self.repository.create(data, website, tag)
        print("Offer created")
        return

    def get_all(
            self,
            page: int = 1,
            page_limit: int = 50,
            query: str = None,
            tag: Optional[str] = None,
    ) -> OfferListOutput:
        """
        Retrieves a paginated list of offers with filtering and sorting options using the OfferRepository.

        Args:
            page (int, optional): The current page number (defaults to 1).
            page_limit (int, optional): The number of offers per page (defaults to 50).
            query (str, optional): A search string to filter offers by title.
            sort_by (OfferSortEnum, optional): The sorting criteria for offers (defaults to newest).

        Returns:
            OfferListOutput: An object containing the list of offers, pagination information,
                             and total number of offers.
        """
        return self.repository.get_all(
            page,
            page_limit,
            query,
            tag
        )

    def change_check_status(self, _id: int, status: bool) -> bool:
        """
        Updates the "checked" status of an offer, raising an exception if the offer is not found.

        Args:
            _id (int): The ID of the offer to update.
            status (bool): The new checked status (True or False).

        Returns:
            bool: True upon successful update, raises HTTPException otherwise.
        """
        if not self.repository.offer_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Offer not found")

        return self.repository.change_check_status(_id, status)

    def get_unique_tags(self) -> List[TagOutput]:
        """
        Retrieves a list of unique tags from the OfferRepository.

        Returns:
            List[str]: A list of unique tags.
        """
        return self.repository.get_unique_tags()


