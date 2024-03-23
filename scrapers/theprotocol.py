import requests
from bs4 import BeautifulSoup
from .abc.scraper_strategy import ScraperStrategy
from typing import Optional, List
from schemas.offer_schema import OfferInput


class TheProtocol(ScraperStrategy):

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        base_url = url
        page_numer = 1
        url = base_url + "&pageNumber=" + str(page_numer)

        offers = []
        while True:
            page_content = requests.get(url).text
            soup = BeautifulSoup(page_content, 'html.parser')

            job_offers = soup.find_all("div", class_="mainWrapper_m12z7gd6")

            if job_offers:
                page_numer += 1
                url = base_url + "&pageNumber=" + str(page_numer)

            if not job_offers:
                break

            for offer in job_offers:
                title = offer.find("h2", class_="titleText_te02th1")
                offer_url = offer.get('href')

                if title and offers:
                    title = title.text
                    offers.append(OfferInput(url=offer_url, title=title))

        return offers

