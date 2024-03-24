import requests
from .abc.scraper_strategy import ScraperStrategy
from typing import Optional, List
from schemas.offer_schema import OfferInput
from datetime import datetime, timedelta
from dateutil.parser import parse


class OLX(ScraperStrategy):
    """
    A class implementing the scraping strategy for OLX website.
    """

    @staticmethod
    def check_date(created_time: str, max_offer_duration_days: int) -> bool:
        parsed_created_time = parse(created_time)
        today = datetime.now(parsed_created_time.tzinfo)
        different = today - parsed_created_time

        result = different.days <= max_offer_duration_days
        print(f"Result: {result}")
        return result

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[OfferInput]]:
        """
        Scrape job offers from OLX website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
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

                if not title or not offer_url:
                    continue

                if max_offer_duration_days:
                    if not self.check_date(d.get("created_time"), max_offer_duration_days):
                        continue

                offers.append(OfferInput(title=title, url=offer_url))

            next_page_element = data.get("links").get("next")

            if not next_page_element:
                break

            if next_page_element:
                base_url = next_page_element.get("href")

        print(f"Scraped {len(offers)} offers")
        return offers
