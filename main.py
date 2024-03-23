from scrapers.abc.scraper import Scraper
from scrapers.bulldogjob import BulldogJob
from scrapers.indeed import Indeed
from utils.init_db import init_db


def main() -> None:
    init_db()

    bulldogjob = Indeed()

    Scraper(bulldogjob).scrape(
        "https://pl.indeed.com/jobs?q=&l=Zdu%C5%84ska%20Wola%2C%20%C5%82%C3%B3dzkie&from=searchOnHP"
    )

if __name__ == '__main__':
    main()
