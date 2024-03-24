from typing import Protocol, List, Optional
from schemas.offer_schema import OfferInput


class ScraperStrategy(Protocol):
    """
    A protocol defining the interface for scraper strategies.
    """
    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        """
        Scrapes data from a given URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        ...
