from typing import List
from sqlalchemy.orm import Session
from models.offer import Offer as OfferModel
from schemas.offer import Offer, OfferOutput, OfferListOutput
from enums.sort_by import OfferSortEnum
from sqlalchemy import asc, desc, func


class OfferRepository:

    def __init__(self, session: Session):
        """
        Initializes the OfferRepository with a database session.

        Args:
            session (sqlalchemy.orm.Session): The database session to use for operations.
        """
        self.session = session

    def create(self, data: Offer, website: str) -> None:
        """
        Creates a new offer in the database.

        Args:
            data (Offer): The offer data to be saved.
            website (str): The website where the offer was found.
        """
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
        """
        Checks if an offer with the given URL already exists in the database.

        Args:
            url (str): The URL of the offer to check.

        Returns:
            bool: True if the offer exists, False otherwise.
        """
        return self.session.query(OfferModel).filter(OfferModel.url == url).first() is not None

    def offer_exists_by_id(self, _id: int) -> bool:
        """
        Checks if an offer with the given ID exists in the database.

        Args:
            _id (int): The ID of the offer to check.

        Returns:
            bool: True if the offer exists, False otherwise.
        """
        return self.session.query(OfferModel).filter(OfferModel.id == _id).first() is not None

    def change_check_status(self, _id: int, status: bool) -> bool:
        """
        Updates the "checked" status of an offer.

        Args:
            _id (int): The ID of the offer to update.
            status (bool): The new checked status (True or False).

        Returns:
            bool: Always True upon successful update.
        """
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
            # sort_by: str = "newest"
    ) -> OfferListOutput:
        """
        Retrieves a paginated list of offers with filtering and sorting options.

        Args:
            page (int, optional): The current page number (defaults to 1).
            page_limit (int, optional): The number of offers per page (defaults to 50).
            query (str, optional): A search string to filter offers by title.
            sort_by (OfferSortEnum, optional): The sorting criteria for offers (defaults to newest).

        Returns:
            OfferListOutput: An object containing the list of offers, pagination information,
                             and total number of offers.
        """

        total_offers_query = self.session.query(func.count(OfferModel.id))

        offers = self.session.query(OfferModel)

        if query is not None:
            offers = offers.filter(OfferModel.title.like(f'%{query}%'))

        offers = offers.order_by(desc(OfferModel.created_at))

        total_offers = total_offers_query.scalar()

        total_pages = (total_offers + page_limit - 1) // page_limit
        prev_page = max(page - 1, 1) if page > 1 else None
        next_page = min(page + 1, total_pages) if page < total_pages else None

        offset = (page - 1) * page_limit if page > 0 else 0
        offers = offers.offset(offset).limit(page_limit).all()

        offers_list = [OfferOutput(**offer.__dict__) for offer in offers]

        return OfferListOutput(
            offers=offers_list,
            prev_page=prev_page,
            next_page=next_page,
            query=query,
            # sort_by=sort_by,
        )