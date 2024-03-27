from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer import Offer
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy


class Jooble(ScraperStrategy):
    """
    A class implementing the scraping strategy for Jooble website.
    """

    @staticmethod
    def check_date(element, max_offer_duration_days: int) -> bool:
        div_element = element.find("div", class_="Vk-5Da")
        if not div_element:
            return False

        text = div_element.text

        if "godzin" in text:
            return True

        if "dni" not in text:
            return False

        num_days = ""
        for word in text.split():
            if word.isdigit():
                num_days += word

        if not num_days:
            return False

        num_days = int(num_days)
        result = num_days <= max_offer_duration_days

        return result

    def parse_offer(self, element, max_offer_duration_days: Optional[int] = None) -> Optional[Offer]:
        """
        Parses job offer data from the HTML element.

        Args:
            element: The HTML element to parse.
            max_offer_duration_days
        Returns:
            Optional[Offer]: The parsed offer input if successful, None otherwise.
        """
        a_element = element.find("a", class_="_8w9Ce2")
        if not a_element:
            return None

        title = a_element.text
        url = a_element.get("href")

        if not title or not url:
            return None

        if max_offer_duration_days and not self.check_date(element, max_offer_duration_days):
            return None

        return Offer(title=title, url=url)

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[Offer]]:
        """
        Scrapes job offers from Jooble website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
        Returns:
            List[Optional[Offer]]: A list of scraped offer inputs.
        """
        base_url = url
        offers = []

        response = get_request(base_url)
        if not response:
            return offers

        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all("div", {"data-test-name": "_jobCard"})
        print(f"Found {len(elements)} elements")

        for element in elements:
            parsed_offer = self.parse_offer(element, max_offer_duration_days)
            if parsed_offer:
                offers.append(parsed_offer)

        print(f"Parsed {len(offers)} offers")
        return offers
