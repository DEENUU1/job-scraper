from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from utils.get_driver import get_driver
from .abc.scraper_strategy import ScraperStrategy


class ITPracujPL(ScraperStrategy):
    """
    A class implementing the scraping strategy for ITPracujPL website.
    """

    @staticmethod
    def parse_data(content: str) -> List[Optional[OfferInput]]:
        """
        Parses job offer data from the HTML content.

        Args:
            content (str): The HTML content to parse.

        Returns:
            List[Optional[OfferInput]]: A list of parsed offer inputs.
        """
        parsed_offers = []
        soup = BeautifulSoup(content, "html.parser")
        offers = soup.find_all("div", class_="be8lukl")
        print(f"Found {len(offers)} offers")

        for offer in offers:
            title = offer.find("h2")
            url = offer.find("a", class_="core_n194fgoq")
            if title and url:
                parsed_offers.append(OfferInput(title=title.text, url=url.get("href")))

        print(f"Parsed {len(parsed_offers)} offers")
        return parsed_offers

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

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        """
        Scrapes job offers from ITPracujPL website.

        Args:
            url (str): The base URL to start scraping from.

        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        print("Run ITPracujPL scraper")
        offers = []
        base_url = url

        driver = get_driver()
        driver.get(base_url)

        page_content = driver.page_source
        parsed_offers = self.parse_data(page_content)
        offers.extend(parsed_offers)
        max_page = self.get_max_page_number(page_content)
        print(f"it.pracuj.pl max page: {max_page}")

        for page in range(2, max_page + 1):
            url = f"{base_url}&pn={page}"
            driver.get(url)
            page_content = driver.page_source
            parsed_offers = self.parse_data(page_content)
            offers.extend(parsed_offers)

        print(f"Scraped {len(offers)} offers")
        return offers
