from typing import Protocol


class ScraperStrategy(Protocol):
    def scrape(self, url: str) -> None:
        ...
