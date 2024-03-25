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
    def check_date(offer, max_offer_duration_days: int) -> bool:
        date_span = offer.find("span", {"data-testid": "myJobsStateDate"})
        if not date_span:
            print("No date span found")
            return False

        date_text = date_span.text.strip()

        if "przed chwilą" in date_text or "Dzisiaj" in date_text:
            return True

        num_of_days = ""
        if "dni temu" in date_text:
            for char in date_text:
                if char.isdigit():
                    num_of_days += char

        if not num_of_days:
            print("Invalid number of days")
            return False

        result = int(num_of_days) <= max_offer_duration_days
        print(f"Result: {result}")

        return result

    def parse_offer(self, offer, max_offer_duration_days: Optional[int] = None) -> Optional[OfferInput]:
        """
        Parses an offer element and extracts relevant information.

        Args:
            offer: The offer element to parse.
            max_offer_duration_days
        Returns:
            Optional[OfferInput]: The parsed offer input if successful, None otherwise.
        """
        offer_url = offer.find("a", class_="jcs-JobTitle")
        if offer_url:
            title = offer_url.find("span")
            if title is None:
                return None

            full_url = f"indeed.com{offer_url.get("href")}"

            if max_offer_duration_days:
                if not self.check_date(offer, max_offer_duration_days):
                    return None

            return OfferInput(url=full_url, title=title.text)

        return None

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[OfferInput]]:
        """
        Scrapes job offers from Indeed website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
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
                parsed_offer = self.parse_offer(offer, max_offer_duration_days)
                if parsed_offer:
                    offers.append(parsed_offer)

            next_page_button = soup.find("a", {"data-testid": "pagination-page-next"})
            if not next_page_button:
                break

            if next_page_button:
                base_url = "https://pl.indeed.com" + next_page_button.get("href")

        print(f"Scraped {len(offers)} offers")
        return offers
