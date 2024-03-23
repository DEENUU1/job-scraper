from .scraper_strategy import ScraperStrategy


class Scraper:
    def __init__(self, strategy: ScraperStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: ScraperStrategy) -> None:
        self._strategy = strategy

    def scrape(self, url: str) -> None:
        return self._strategy.scrape(url)
