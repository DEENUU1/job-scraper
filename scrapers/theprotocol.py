from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer import Offer
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy


class TheProtocol(ScraperStrategy):
    """
    A class implementing the scraping strategy for TheProtocol website.
    """

    @staticmethod
    def remove_search_id(url: str) -> str:
        url_parts = url.split("?")
        return url_parts[0]

    def parse_offer(self, offer) -> Optional[Offer]:
        """
        Parse a job offer from the HTML representation.

        Args:
            offer: HTML representation of the job offer.

        Returns:
            Optional[Offer]: Parsed job offer input.
        """
        title = offer.find("h2", class_="titleText_te02th1")
        offer_url = offer.get("href")

        if not title or not offer_url:
            return None

        full_url = f"https://theprotocol.it{offer_url}"
        processed_url = self.remove_search_id(full_url)
        return Offer(url=processed_url, title=title.text)

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[Offer]]:
        """
        Scrape job offers from TheProtocol website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days (int)
        Returns:
            List[Optional[Offer]]: A list of scraped offer inputs.
        """
        base_url = url
        page_number = 1
        offers = []

        while True:
            url = f"{base_url}&pageNumber={page_number}"
            response = get_request(url)

            if not response:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            job_offers = soup.find_all("a", class_="anchorClass_aqdsolh")
            print(f"Found {len(job_offers)} job offers")

            for offer in job_offers:
                parsed_offer = self.parse_offer(offer)
                if parsed_offer:
                    offers.append(parsed_offer)

            page_number += 1

            if not job_offers:
                break

        print(f"Parsed {len(offers)} offers")
        return offers
