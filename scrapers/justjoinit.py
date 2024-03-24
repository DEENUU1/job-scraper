import time
from typing import Optional, List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from schemas.offer_schema import OfferInput
from utils.get_driver import get_driver
from .abc.scraper_strategy import ScraperStrategy


class JustJoinIT(ScraperStrategy):
    """
    A class implementing the scraping strategy for JustJoinIT website.
    """

    @staticmethod
    def get_content(driver) -> List[Optional[str]]:
        """
        Retrieves the HTML content of job offer elements from the webpage.

        Args:
            driver: The Selenium WebDriver instance.

        Returns:
            List[Optional[str]]: A list of HTML content strings.
        """
        data = []
        last_height = 0
        while True:
            elements = driver.find_elements(By.CLASS_NAME, "css-2crog7")
            print(f"Found {len(elements)} elements")

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
        return data

    @staticmethod
    def parse_offers(data) -> List[Optional[OfferInput]]:
        """
        Parses job offer data from HTML content.

        Args:
            data (List[Optional[str]]): A list of HTML content strings.

        Returns:
            List[Optional[OfferInput]]: A list of parsed offer inputs.
        """
        unique_urls = []
        offers = []
        for d in data:
            soup = BeautifulSoup(d, "html.parser")
            title = soup.find("h2")
            url = soup.find("a")

            if title and url:
                title = title.text
                url = url.get("href")

                if url not in unique_urls and title:
                    unique_urls.append(url)

                    full_url = f"justjoin.it{url}"
                    offers.append(OfferInput(title=title, url=full_url))
        return offers

    def scrape(self, url: str) -> List[Optional[OfferInput]]:
        """
        Scrapes job offers from JustJoinIT website.

        Args:
            url (str): The base URL to start scraping from.

        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        print("Run JustJoinIT scraper")

        driver = get_driver()
        driver.get(url)

        data = self.get_content(driver)
        parsed_offers = self.parse_offers(data)

        print(f"Scraped {len(parsed_offers)} offers")
        return parsed_offers
