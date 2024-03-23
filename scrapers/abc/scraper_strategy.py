from typing import Protocol, List, Optional
from schemas.offer_schema import OfferInput


class ScraperStrategy(Protocol):
    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        ...
