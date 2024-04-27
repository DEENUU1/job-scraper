from typing import Optional, List
from bs4 import BeautifulSoup
from schemas.offer import Offer
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
            return False

        result = int(num_of_days) <= max_offer_duration_days
        return result

    def parse_offer(self, offer, max_offer_duration_days: Optional[int] = None) -> Optional[Offer]:
        """
        Parses an offer element and extracts relevant information.

        Args:
            offer: The offer element to parse.
            max_offer_duration_days
        Returns:
            Optional[Offer]: The parsed offer input if successful, None otherwise.
        """
        offer_url = offer.find("a", class_="jcs-JobTitle")
        if not offer_url:
            return None

        title = offer_url.find("span")
        if title is None:
            return None

        full_url = f"https://indeed.com{offer_url.get("href")}"
        processed_url = self.process_url(full_url)

        if processed_url is None:
            return None

        if max_offer_duration_days and not self.check_date(offer, max_offer_duration_days):
            return None

        return Offer(url=str(processed_url), title=str(title.text))

    @staticmethod
    def process_url(url: str) -> str:
        base_url, query_string = url.split("?")

        query_params = query_string.split("&")

        jk_value = None

        for param in query_params:
            try:
                key, value = param.split("=")
                if key == "jk":
                    jk_value = value
                    break
            except ValueError:
                pass

        result = f"indeed.com/rc/clk?jk={jk_value}&bb=" if jk_value else None
        return result

    @staticmethod
    def get_next_url(soup) -> Optional[str]:
        next_page_button = soup.find("a", {"data-testid": "pagination-page-next"})
        if not next_page_button:
            return None

        return "https://pl.indeed.com" + next_page_button.get("href")

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[Offer]]:
        """
        Scrapes job offers from Indeed website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
        Returns:
            List[Optional[Offer]]: A list of scraped offer inputs.
        """
        offers = []
        base_url = url

        driver = get_driver()

        while True:
            driver.get(base_url)
            page_source = driver.page_source

            if not page_source:
                break

            print(f"Successfully visited: {url}")

            soup = BeautifulSoup(page_source, "html.parser")
            job_elements = soup.find_all("li", class_="css-5lfssm")

            print(f"Found {len(job_elements)} elements")

            for offer in job_elements:
                parsed_offer = self.parse_offer(offer, max_offer_duration_days)
                if parsed_offer:
                    offers.append(parsed_offer)

            next_url = self.get_next_url(soup)
            if not next_url:
                break
            base_url = next_url

        print(f"Parsed {len(offers)} offers")

        driver.quit()
        return offers
