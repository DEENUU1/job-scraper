from typing import List, Optional
import gspread
from scrapers.abc.scraper import Scraper
from utils.map_url_to_scraper import url_to_scraper
import time
from utils.urls_to_skip import get_urls_to_skip
from utils.validate_title_keywords import check_title
from googlesheet.googlesheet import GoogleSheet


def run_all_scraper(
        websites: List[Optional[str]],
        worksheet_url: str,
        max_offer_duration_days: Optional[int] = None,
        keywords_to_pass: List[Optional[str]] = None,
) -> None:
    """
    Runs all scrapers for the given list of websites and adds scraped data to the specified Google Sheet.

    Args:
        websites (List[Optional[str]]): A list of website URLs to scrape.
        worksheet_url (str) The worksheet url.
        max_offer_duration_days
        keywords_to_pass (List[Optional[str]])
    Returns:
        None
    """
    urls_to_skip = get_urls_to_skip()

    if not websites:
        print("No websites to scrape")
        return

    for url in websites:
        scraper_class, website = url_to_scraper(url)
        if not scraper_class:
            print("Invalid URL or website is not supported")
            return

        scraped_offers = Scraper(scraper_class).scrape(url, max_offer_duration_days)
        print(len(scraped_offers))
        for offer in scraped_offers:
            if offer.url in urls_to_skip:
                print("Offer skipped")
                continue

            if check_title(offer.title, keywords_to_pass):
                print(f"Offer skipped: {offer.title}")
                continue

            gs = GoogleSheet(worksheet_url)

            if gs.data_exists(2, offer.url):
                print("Offer exists in google sheet")
                time.sleep(2)  # Rate limit Google Sheet API (60 requests per minute)
                continue

            time.sleep(2)  # Rate limit Google Sheet API (60 requests per minute)

            gs.add_data(data=offer, website=website)
