from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer_schema import OfferInput
from .abc.scraper_strategy import ScraperStrategy
from utils.get_driver import get_driver


class Indeed(ScraperStrategy):

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        driver = get_driver()

        offers = []
        base_url = url

        while True:
            driver.get(base_url)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            job_elements = soup.find_all("li", class_="css-5lfssm")

            for offer in job_elements:
                offer_url = offer.find("a", class_="jcs-JobTitle")
                if offer_url:
                    title = offer_url.find("span")
                    if title:
                        offers.append(OfferInput(url=offer_url.get("href"), title=title.text))

            next_page_button = soup.find("a", {"data-testid": "pagination-page-next"})
            if not next_page_button:
                break

            if next_page_button:
                base_url = "https://pl.indeed.com" + next_page_button.get("href")

        return offers
