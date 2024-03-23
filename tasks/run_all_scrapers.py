from services.website_service import WebsiteService
from services.offer_service import OfferService
from scrapers.abc.scraper import Scraper
from sqlalchemy.orm import Session
from utils.map_url_to_scraper import url_to_scraper


def run_all_scraper(session: Session) -> None:
    websites = WebsiteService(session).get_all_websites()

    for website in websites:
        scraper_class = url_to_scraper(website.url)
        if not scraper_class:
            return

        scraped_offers = Scraper(scraper_class).scrape(website.url)

        for offer in scraped_offers:
            created_offer = OfferService(session).create(offer, website.id)
            print(created_offer)
