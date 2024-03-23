from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .abc.scraper_strategy import ScraperStrategy


class Indeed(ScraperStrategy):

    def scrape(self, url: str) -> None:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


        offers = []
        base_url = url

        while True:
            driver.get(base_url)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            job_elements = soup.find_all("li", class_="css-5lfssm")

            for offer in job_elements:
                offer_url = offer.find("a", class_="jcs-JobTitle")
                if offer_url:
                    title = offer_url.find("span")

                    d = {"url": offer_url.get("href"), "title": title.text}
                    print(d)
                    offers.append(d)

            next_page_button = soup.find("a", {"data-testid": "pagination-page-next"})
            if not next_page_button:
                break

            if next_page_button:
                base_url = "https://pl.indeed.com" + next_page_button.get("href")

        print(offers)
        print(len(offers))