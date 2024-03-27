from typing import List, Optional

from bs4 import BeautifulSoup

from schemas.offer import Offer
from utils.get_driver import get_driver
from .abc.scraper_strategy import ScraperStrategy


class PracujPlBase(ScraperStrategy):

    @staticmethod
    def remove_search_id(url: str) -> str:
        url_parts = url.split("?")
        return url_parts[0]

    @staticmethod
    def get_max_page_number(content: str) -> int:
        """
        Retrieves the maximum page number from the HTML content.

        Args:
            content (str): The HTML content containing pagination information.

        Returns:
            int: The maximum page number.
        """
        try:
            soup = BeautifulSoup(content, "html.parser")
            max_page_element = soup.find(
                "span", {"data-test": "top-pagination-max-page-number"}
            )
            if max_page_element:
                return int(max_page_element.text)
        except Exception as e:
            print(e)

        return 1

    def parse_data(self, content: str) -> List[Optional[Offer]]:
        pass

    @staticmethod
    def close_modal(driver) -> None:
        pass

    def get_page_content(self, driver, base_url: str) -> Optional[str]:
        pass

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[Offer]]:
        """
        Scrapes job offers from ITPracujPL website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
        Returns:
            List[Optional[Offer]]: A list of scraped offer inputs.
        """
        offers = []
        base_url = url

        driver = get_driver()

        page_content = self.get_page_content(driver, base_url)
        if not page_content:
            return []

        parsed_offers = self.parse_data(page_content)
        offers.extend(parsed_offers)

        max_page = self.get_max_page_number(page_content)
        for page in range(2, max_page + 1):
            url = f"{base_url}&pn={page}"

            page_content = self.get_page_content(driver, url)
            if not page_content:
                break

            parsed_offers = self.parse_data(page_content)
            offers.extend(parsed_offers)

        print(f"Parsed {len(offers)} offers")
        return offers
