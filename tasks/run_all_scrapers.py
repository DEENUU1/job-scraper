import time
from typing import List, Optional

from config.database import get_db
from export.googlesheet import GoogleSheet
from scrapers.abc.scraper import Scraper
from utils.map_url_to_scraper import url_to_scraper
from utils.urls_to_skip import get_urls_to_skip
from utils.validate_title_keywords import check_title
from export.excel import ExcelWriter
from service.offer_service import OfferService


def run_all_scraper(
        websites: List[Optional[str]],
        worksheet_url: str,
        export_type: str = "excel",  # or 'googlesheet' or 'db'
        max_offer_duration_days: Optional[int] = None,
        keywords_to_pass: List[Optional[str]] = None,
) -> None:
    """
    Runs all scrapers for the given list of websites and adds scraped data to the specified Google Sheet.

    Args:
        websites (List[Optional[str]]): A list of website URLs to scrape.
        worksheet_url (str) The worksheet url.
        export_type (str)
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
            continue

        scraped_offers = Scraper(scraper_class).scrape(url, max_offer_duration_days)
        for offer in scraped_offers:
            if offer.url in urls_to_skip:
                print("Offer skipped")
                continue

            if check_title(offer.title, keywords_to_pass):
                print(f"Offer skipped: {offer.title}")
                continue

            if export_type == "excel":
                ew = ExcelWriter()

                if ew.data_exists(url=offer.url):
                    print("Offer exists in excel")
                    continue

                ew.add_data(data=offer, website=website)
                ew.save()

            elif export_type == "googlesheet":
                gs = GoogleSheet(worksheet_url)

                if gs.data_exists(2, offer.url):
                    print("Offer exists in google sheet")
                    # Rate limit Google Sheet API (60 requests per minute)
                    time.sleep(2)
                    continue

                # Rate limit Google Sheet API (60 requests per minute)
                time.sleep(2)

                gs.add_data(data=offer, website=website)

            elif export_type == "db":
                offer_service = OfferService(next(get_db()))
                offer_service.create(offer, website)


            else:
                raise ValueError("Invalid export type")
