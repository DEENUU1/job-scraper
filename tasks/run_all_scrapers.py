from typing import List, Optional
import gspread
from googlesheet.add_to_gs import add_data_to_sheet
from scrapers.abc.scraper import Scraper
from utils.map_url_to_scraper import url_to_scraper
import time
from utils.urls_to_skip import get_urls_to_skip
from googlesheet.url_exists import url_exist


def run_all_scraper(
        websites: List[Optional[str]],
        worksheet: gspread.Worksheet,
        max_offer_duration_days: Optional[int] = None
) -> None:
    """
    Runs all scrapers for the given list of websites and adds scraped data to the specified Google Sheet.

    Args:
        websites (List[Optional[str]]): A list of website URLs to scrape.
        worksheet (gspread.Worksheet): The worksheet to add scraped data to.
        max_offer_duration_days
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

            if url_exist(worksheet, 2, offer.url):
                print("Offer exists in google sheet")
                continue

            time.sleep(1)  # Rate limit Google Sheet API (60 requests per minute)

            add_data_to_sheet(data=offer, website=website, worksheet=worksheet)
