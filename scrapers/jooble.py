import requests
from bs4 import BeautifulSoup
from .abc.scraper_strategy import ScraperStrategy


class Jooble(ScraperStrategy):
    def scrape(self, url: str) -> None:
        base_url = url
        offers = []

        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, "html.parser")

        elements = soup.find_all("div", class_="MhjGza")
        for element in elements:
            a_element = element.find("a", class_="_8w9Ce2")

            if a_element:
                title = a_element.text
                url = a_element.get("href")
                offers.append({"url": url, "title": title})

        print(len(offers))
