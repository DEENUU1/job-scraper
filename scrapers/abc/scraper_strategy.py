from typing import Protocol, List, Optional
from schemas.offer_schema import OfferInput


class ScraperStrategy(Protocol):
    """
    A protocol defining the interface for scraper strategies.
    """
    def scrape(
            self,
            url: str,
            max_offer_duration_days: Optional[int] = None
    ) -> List[Optional[OfferInput]]:
        """
        Scrapes data from a given URL.

        Args:
            url (str): The URL to scrape.
            max_offer_duration_days (int): The maximum number of days
        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        ...
