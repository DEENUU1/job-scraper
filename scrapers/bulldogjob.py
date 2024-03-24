from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy


class BulldogJob(ScraperStrategy):
    """
    A class implementing the scraping strategy for BulldogJob website.
    """

    @staticmethod
    def parse_offer(offer) -> Optional[OfferInput]:
        """
        Parses an offer element and extracts relevant information.

        Args:
            offer: The offer element to parse.

        Returns:
            Optional[OfferInput]: The parsed offer input if successful, None otherwise.
        """
        title = offer.find("h3")
        job_url = offer.get("href")

        if title and job_url:
            return OfferInput(title=title.text, url=job_url)
        return None

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        """
        Scrapes job offers from BulldogJob website.

        Args:
            url (str): The base URL to start scraping from.

        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        print("Run BulldogJob scraper")

        page_num = 1
        offers = []

        previous_page = None
        while True:
            base_url = f"{url}{page_num}"
            response = get_request(base_url)
            print(f"Status code: {response.status_code}")

            soup = BeautifulSoup(response.text, "html.parser")

            job_offers = soup.find_all("a", class_="JobListItem_item__M79JI")
            print(f"Found {len(job_offers)} offers")

            if previous_page == job_offers:
                break

            previous_page = job_offers

            if not job_offers:
                break

            if job_offers:
                page_num += 1

            for offer in job_offers:
                parsed_offer = self.parse_offer(offer)
                if parsed_offer:
                    offers.append(parsed_offer)

        print(f"Scraped {len(offers)} offers")
        return offers
