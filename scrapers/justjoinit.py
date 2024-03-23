import time
from typing import Optional, List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from schemas.offer_schema import OfferInput
from utils.get_driver import get_driver
from .abc.scraper_strategy import ScraperStrategy


class JustJoinIT(ScraperStrategy):

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        driver = get_driver()
        driver.get(url)
        data = []
        last_height = 0
        while True:
            elements = driver.find_elements(By.CLASS_NAME, "css-2crog7")
            if elements:
                for element in elements:
                    data.append(element.get_attribute("outerHTML"))
            driver.execute_script(
                f"window.scrollBy(0, 500);"
            )
            time.sleep(1)

            new_height = driver.execute_script("return window.scrollY")
            if new_height == last_height:
                break
            last_height = new_height

        urls = []
        offers = []
        for d in data:
            soup = BeautifulSoup(d, "html.parser")
            title = soup.find("h2")
            url = soup.find("a")

            if title and url:
                title = title.text
                url = url.get("href")

                if url not in urls and title:
                    urls.append(url)

                    offers.append(OfferInput(title=title, url=url))

        return offers
