from typing import Optional, List

import requests
from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from .abc.scraper_strategy import ScraperStrategy


class BulldogJob(ScraperStrategy):

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        page_num = 1

        offers = []

        while True:
            base_url = f"{url}{page_num}"

            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, "html.parser")

            job_offers = soup.find_all("a", class_="JobListItem_item__M79JI")

            if not job_offers:
                break

            if job_offers:
                page_num += 1

            for offer in job_offers:
                title = offer.find("h3")
                job_url = offer.get("href")

                if title and job_url:
                    offers.append(OfferInput(title=title.text, url=job_url))

        return offers
