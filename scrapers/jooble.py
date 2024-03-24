from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy


class Jooble(ScraperStrategy):
    """
    A class implementing the scraping strategy for Jooble website.
    """

    @staticmethod
    def parse_offer(element) -> Optional[OfferInput]:
        """
        Parses job offer data from the HTML element.

        Args:
            element: The HTML element to parse.

        Returns:
            Optional[OfferInput]: The parsed offer input if successful, None otherwise.
        """
        a_element = element.find("a", class_="_8w9Ce2")

        if a_element:
            title = a_element.text
            url = a_element.get("href")
            if title and url:
                return OfferInput(title=title, url=url)

        return None

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        """
        Scrapes job offers from Jooble website.

        Args:
            url (str): The base URL to start scraping from.

        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        print("Run Jooble scraper")

        base_url = url
        offers = []

        response = get_request(base_url)
        print(f"Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")

        elements = soup.find_all("div", class_="MhjGza")
        print(f"Found {len(elements)} elements")

        for element in elements:
            parsed_offer = self.parse_offer(element)
            if parsed_offer:
                offers.append(parsed_offer)

        print(f"Scraped {len(offers)} offers")
        return offers
