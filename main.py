from utils.init_db import init_db
from config.database import get_db
from services.website_service import WebsiteService
from schemas.website_schema import WebsiteInput
from tasks.run_all_scrapers import run_all_scraper


def main() -> None:
    init_db()

    session = next(get_db())
    # website_1 = WebsiteInput(url="https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=4&region_id=7&city_id=41415&sort_by=created_at%3Adesc&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5")
    # created_website = WebsiteService(session).create(website_1)
    # print(created_website)

    run_all_scraper(session)

if __name__ == '__main__':
    main()
