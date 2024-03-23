import requests
from .abc.scraper_strategy import ScraperStrategy


class OLX(ScraperStrategy):

    def scrape(self, url: str) -> None:
        base_url = url
        offers = []
        while True:
            response = requests.get(base_url)
            data = response.json()

            for d in data["data"]:
                offers.append({"title": d["title"], "url": d["url"]})

            next_page_element = data.get("links").get("next")

            if not next_page_element:
                break

            if next_page_element:
                base_url = next_page_element.get("href")

        print(len(offers))