from typing import List, Optional

from googlesheet.add_to_gs import add_data_to_sheet
from scrapers.abc.scraper import Scraper
from utils.map_url_to_scraper import url_to_scraper
import gspread


def run_all_scraper(
        websites: List[Optional[str]],
        worksheet: gspread.Worksheet
) -> None:
    if not websites:
        print("No websites to scrape")
        return

    for url in websites:
        scraper_class = url_to_scraper(url)
        if not scraper_class:
            print("Invalid url or website is not supported")
            return

        scraped_offers = Scraper(scraper_class).scrape(url)

        for offer in scraped_offers:
            add_data_to_sheet(data=offer, worksheet=worksheet)
