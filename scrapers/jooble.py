from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy


class Jooble(ScraperStrategy):
    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        base_url = url
        offers = []

        response = get_request(base_url)
        soup = BeautifulSoup(response.text, "html.parser")

        elements = soup.find_all("div", class_="MhjGza")
        for element in elements:
            a_element = element.find("a", class_="_8w9Ce2")

            if a_element:
                title = a_element.text
                url = a_element.get("href")
                if title and url:
                    offers.append(OfferInput(title=title, url=url))

        return offers
