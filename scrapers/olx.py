import requests
from .abc.scraper_strategy import ScraperStrategy
from typing import Optional, List
from schemas.offer_schema import OfferInput


class OLX(ScraperStrategy):
    """
    A class implementing the scraping strategy for OLX website.
    """
    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        """
        Scrape job offers from OLX website.

        Args:
            url (str): The base URL to start scraping from.

        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        print("Run OLX scraper")

        base_url = url
        offers = []

        while True:
            response = requests.get(base_url)
            print(f"Status code: {response.status_code}")
            data = response.json()

            for d in data["data"]:
                title = d.get("title")
                offer_url = d.get("url")

                offers.append(OfferInput(title=title, url=offer_url))

            next_page_element = data.get("links").get("next")

            if not next_page_element:
                break

            if next_page_element:
                base_url = next_page_element.get("href")

        print(f"Scraped {len(offers)} offers")
        return offers
