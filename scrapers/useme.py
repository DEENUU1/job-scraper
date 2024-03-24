from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy


class Useme(ScraperStrategy):
    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        print("Run Useme scraper")

        base_url = url
        url = base_url
        offers = []

        while True:
            response = get_request(url)
            print(f"Status code: {response.status_code}")

            soup = BeautifulSoup(response.text, "html.parser")

            jobs_div = soup.find_all("div", class_="job")
            print(f"Found {len(jobs_div)} jobs")

            for job in jobs_div:
                title = job.find("h2", class_="job__title").text
                offer_url = job.find("a", class_="job__title-link").get("href")

                full_offer_url = f"useme.com{offer_url}"
                offers.append(OfferInput(title=title, url=full_offer_url))

            next_page_url = soup.find("a", rel="next")
            if not next_page_url:
                break

            if next_page_url:
                url = base_url + next_page_url.get("href")

        print(f"Scraped {len(offers)} offers")
        return offers
