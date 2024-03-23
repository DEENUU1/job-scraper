
from scrapers.abc.scraper import Scraper
from sqlalchemy.orm import Session
from utils.map_url_to_scraper import url_to_scraper


def run_all_scraper() -> None:
    websites = ...  # TODO read it from file

    for website in websites:
        scraper_class = url_to_scraper(website.url)
        if not scraper_class:
            return

        scraped_offers = Scraper(scraper_class).scrape(website.url)

        for offer in scraped_offers:
            print(offer)
