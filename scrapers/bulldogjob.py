from typing import Optional, List

import requests
from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from .abc.scraper_strategy import ScraperStrategy
from utils.get_request import get_request


class BulldogJob(ScraperStrategy):

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
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
                title = offer.find("h3")
                job_url = offer.get("href")

                if title and job_url:
                    offers.append(OfferInput(title=title.text, url=job_url))

        print(f"Scraped {len(offers)} offers")
        return offers
