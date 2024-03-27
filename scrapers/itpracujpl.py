from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer import Offer
from .pracujpl_base import PracujPlBase


class ITPracujPL(PracujPlBase):
    """
    A class implementing the scraping strategy for ITPracujPL website.
    """

    def parse_data(self, content: str) -> List[Optional[Offer]]:
        """
        Parses job offer data from the HTML content.

        Args:
            content (str): The HTML content to parse.

        Returns:
            List[Optional[Offer]]: A list of parsed offer inputs.
        """
        parsed_offers = []

        soup = BeautifulSoup(content, "html.parser")
        offers = soup.find_all("div", class_="be8lukl")
        print(f"Found {len(offers)} offers")

        for offer in offers:
            title = offer.find("h2")
            url = offer.find("a", class_="core_n194fgoq")

            if not title or not url:
                continue

            processed_url = self.remove_search_id(url.get("href"))
            parsed_offers.append(Offer(title=title.text, url=processed_url))

        print(f"Parsed {len(parsed_offers)} offers")
        return parsed_offers

    def get_page_content(self, driver, base_url: str) -> Optional[str]:
        driver.get(base_url)
        page_content = driver.page_source
        if not page_content:
            return None

        print(f"Successfully visited: {base_url}")
        return page_content
