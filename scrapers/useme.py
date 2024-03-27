from typing import Optional, List

from bs4 import BeautifulSoup

from schemas.offer import Offer
from utils.get_request import get_request
from .abc.scraper_strategy import ScraperStrategy
from datetime import datetime, timedelta


class Useme(ScraperStrategy):
    """
    A class implementing the scraping strategy for Useme website.
    """

    @staticmethod
    def check_date(job, max_offer_duration_days: int) -> bool:
        date_div = job.find("div", class_="job__header-details--date")
        if not date_div:
            return False

        span_elements = date_div.find_all("span")
        if len(span_elements) != 2:
            return False

        date_str = span_elements[1].text.strip()
        if date_str == "Zakończone":
            return False

        date = datetime.strptime(date_str, "%d.%m.%y")

        today = datetime.now()
        difference = today - date

        result = difference.days <= max_offer_duration_days

        return result

    def parse_offer(self, job, max_offer_duration_days: Optional[int] = None) -> Optional[Offer]:
        """
        Parse a job offer from the HTML representation.

        Args:
            job: HTML representation of the job offer.
            max_offer_duration_days
        Returns:
            Optional[Offer]: Parsed job offer input.
        """
        title = job.find("h2", class_="job__title")
        offer_url = job.find("a", class_="job__title-link")

        if not title or not offer_url:
            return None

        if max_offer_duration_days and not self.check_date(job, max_offer_duration_days):
            return None

        full_offer_url = f"useme.com{offer_url.get("href")}"
        return Offer(title=title.text, url=full_offer_url)

    @staticmethod
    def get_next_page_url(soup, base_url) -> Optional[str]:
        next_page_url = soup.find("a", rel="next")
        if not next_page_url:
            return None

        return base_url + next_page_url.get("href")

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[Offer]]:
        """
        Scrape job offers from Useme website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
        Returns:
            List[Optional[Offer]]: A list of scraped offer inputs.
        """
        base_url = url
        url = base_url
        offers = []

        while True:
            response = get_request(url)
            if not response:
                break

            soup = BeautifulSoup(response.text, "html.parser")

            jobs_div = soup.find_all("div", class_="job")
            print(f"Found {len(jobs_div)} jobs")

            for job in jobs_div:
                parsed_offer = self.parse_offer(job, max_offer_duration_days)
                if parsed_offer:
                    offers.append(parsed_offer)

            next_page_url = self.get_next_page_url(soup, base_url)
            if not next_page_url:
                break

            url = next_page_url

        print(f"Parsed {len(offers)} offers")
        return offers
