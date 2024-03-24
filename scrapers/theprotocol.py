from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy


class TheProtocol(ScraperStrategy):
    """
    A class implementing the scraping strategy for TheProtocol website.
    """

    @staticmethod
    def parse_offer(offer) -> Optional[OfferInput]:
        """
        Parse a job offer from the HTML representation.

        Args:
            offer: HTML representation of the job offer.

        Returns:
            Optional[OfferInput]: Parsed job offer input.
        """
        title = offer.find("h2", class_="titleText_te02th1")
        offer_url = offer.get("href")

        if title and offer_url:
            title = title.text
            return OfferInput(url=offer_url, title=title)

        return None

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        """
        Scrape job offers from TheProtocol website.

        Args:
            url (str): The base URL to start scraping from.

        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        print("Run TheProtocol scraper")

        base_url = url
        page_number = 1
        offers = []

        while True:
            url = f"{base_url}&pageNumber={page_number}"
            response = get_request(url)
            print(f"Status code: {response.status_code}")

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

        print(f"Scraped {len(offers)} offers")
        return offers
