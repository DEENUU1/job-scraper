from .scraper_strategy import ScraperStrategy
from typing import List, Optional
from schemas.offer_schema import OfferInput


class Scraper:
    def __init__(self, strategy: ScraperStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: ScraperStrategy) -> None:
        self._strategy = strategy

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        return self._strategy.scrape(url)
