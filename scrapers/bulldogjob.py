from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer import Offer
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy


class BulldogJob(ScraperStrategy):
    """
    A class implementing the scraping strategy for BulldogJob website.
    """

    @staticmethod
    def parse_offer(offer) -> Optional[Offer]:
        """
        Parses an offer element and extracts relevant information.

        Args:
            offer: The offer element to parse.

        Returns:
            Optional[Offer]: The parsed offer input if successful, None otherwise.
        """
        title = offer.find("h3")
        job_url = offer.get("href")

        if title and job_url:
            return Offer(title=title.text, url=job_url)
        return None

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[Offer]]:
        """
        Scrapes job offers from BulldogJob website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
        Returns:
            List[Optional[Offer]]: A list of scraped offer inputs.
        """

        page_num = 1
        offers = []
        previous_page = None

        while True:
            base_url = f"{url}{page_num}"
            response = get_request(base_url)

            if not response:
                break

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

        print(f"Parsed {len(offers)} offers")
        return offers
