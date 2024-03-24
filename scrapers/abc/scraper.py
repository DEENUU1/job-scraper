from .scraper_strategy import ScraperStrategy
from typing import List, Optional
from schemas.offer_schema import OfferInput


class Scraper:
    """
    A class representing a web scraper.

    Attributes:
        _strategy (ScraperStrategy): The strategy used for scraping.
    """
    def __init__(self, strategy: ScraperStrategy) -> None:
        """
        Initializes the Scraper with a given strategy.

        Args:
            strategy (ScraperStrategy): The strategy used for scraping.

        Returns:
            None
        """
        self._strategy = strategy

    def set_strategy(self, strategy: ScraperStrategy) -> None:
        """
        Sets the strategy used for scraping.

        Args:
            strategy (ScraperStrategy): The strategy used for scraping.

        Returns:
            None
        """
        self._strategy = strategy

    def scrape(
            self,
            url: str,
            max_offer_duration_days: Optional[int] = None
    ) -> List[Optional[OfferInput]]:
        """
        Scrapes data from a given URL using the current strategy.

        Args:
            url (str): The URL to scrape.
            max_offer_duration_days (int): The maximum number of days
        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        return self._strategy.scrape(url, max_offer_duration_days)
