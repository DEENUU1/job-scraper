import requests
from bs4 import BeautifulSoup

from .abc.scraper_strategy import ScraperStrategy


class Useme(ScraperStrategy):
    def scrape(self, url: str) -> None:
        base_url = url
        url = base_url
        jobs = []

        while True:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            jobs_div = soup.find_all("div", class_="job")
            for job in jobs_div:
                title = job.find("h2", class_="job__title").text
                offer_url = job.find("a", class_="job__title-link").get("href")

                jobs.append({"title": title, "url": offer_url})

            next_page_url = soup.find("a", rel="next")
            if not next_page_url:
                break

            if next_page_url:
                url = base_url + next_page_url.get("href")

        print(len(jobs))
