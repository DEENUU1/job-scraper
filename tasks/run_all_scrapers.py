from typing import List, Optional

import gspread

from googlesheet.add_to_gs import add_data_to_sheet
from scrapers.abc.scraper import Scraper
from utils.map_url_to_scraper import url_to_scraper


def run_all_scraper(
        websites: List[Optional[str]],
        worksheet: gspread.Worksheet
) -> None:
    if not websites:
        print("No websites to scrape")
        return

    for url in websites:
        scraper_class, website = url_to_scraper(url)
        if not scraper_class:
            print("Invalid url or website is not supported")
            return

        scraped_offers = Scraper(scraper_class).scrape(url)
        print(len(scraped_offers))
        for offer in scraped_offers:
            print("Add scraped offers to Google Sheet")
            add_data_to_sheet(data=offer, website=website, worksheet=worksheet)
