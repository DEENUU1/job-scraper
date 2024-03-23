from scrapers.abc.scraper import Scraper
from scrapers.bulldogjob import BulldogJob
from scrapers.indeed import Indeed


def main() -> None:
    bulldogjob = Indeed()

    Scraper(bulldogjob).scrape(
        "https://pl.indeed.com/jobs?q=&l=Zdu%C5%84ska%20Wola%2C%20%C5%82%C3%B3dzkie&from=searchOnHP"
    )

if __name__ == '__main__':
    main()
