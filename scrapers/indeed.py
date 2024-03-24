from typing import Optional, List
from bs4 import BeautifulSoup
from schemas.offer_schema import OfferInput
from .abc.scraper_strategy import ScraperStrategy
from utils.get_driver import get_driver


class Indeed(ScraperStrategy):
    """
    A class implementing the scraping strategy for Indeed website.
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
        offer_url = offer.find("a", class_="jcs-JobTitle")
        if offer_url:
            title = offer_url.find("span")
            if title:
                full_offer_url = f"indeed.com{offer_url.get('href')}"
                return OfferInput(url=full_offer_url, title=title.text)

        return None

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        """
        Scrapes job offers from Indeed website.

        Args:
            url (str): The base URL to start scraping from.

        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        print("Run Indeed scraper")

        offers = []
        base_url = url

        driver = get_driver()

        while True:
            driver.get(base_url)

            page_source = driver.page_source

            soup = BeautifulSoup(page_source, "html.parser")
            job_elements = soup.find_all("li", class_="css-5lfssm")
            print(f"Found {len(job_elements)} elements")

            for offer in job_elements:
                parsed_offer = self.parse_offer(offer)
                if parsed_offer:
                    offers.append(parsed_offer)

            next_page_button = soup.find("a", {"data-testid": "pagination-page-next"})
            if not next_page_button:
                break

            if next_page_button:
                base_url = "https://pl.indeed.com" + next_page_button.get("href")

        print(f"Scraped {len(offers)} offers")
        return offers
