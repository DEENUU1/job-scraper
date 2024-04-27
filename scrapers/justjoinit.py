import time
from typing import Optional, List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from schemas.offer import Offer
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
    def check_date(offer, max_offer_duration_days: int) -> bool:
        date_element = offer.find("div", class_="css-1am4i4o")
        if not date_element:
            print("No date element found")
            return False

        date_text = date_element.text

        if date_text == "New":
            print("Offer is new")
            return True

        num_of_days = ""
        if "d" in date_text:
            for char in date_text:
                if char.isdigit():
                    num_of_days += char

        if not num_of_days:
            print("Invalid number of days")
            return False

        result = int(num_of_days) <= max_offer_duration_days
        print(f"Result: {result}")
        return result

    def parse_offers(
            self,
            data: List[Optional[str]],
            max_offer_duration_days: Optional[int] = None
    ) -> List[Optional[Offer]]:
        """
        Parses job offer data from HTML content.

        Args:
            data (List[Optional[str]]): A list of HTML content strings.
            max_offer_duration_days
        Returns:
            List[Optional[Offer]]: A list of parsed offer inputs.
        """
        if not data:
            return []

        unique_urls, offers = [], []

        for d in data:
            soup = BeautifulSoup(d, "html.parser")
            title = soup.find("h2")
            url = soup.find("a")

            if not title or not url:
                continue

            title = title.text
            url = url.get("href")

            if max_offer_duration_days and not self.check_date(soup, max_offer_duration_days):
                continue

            if url in unique_urls:
                continue

            unique_urls.append(url)
            full_url = f"https://justjoin.it{url}"
            offers.append(Offer(title=title, url=full_url))

        return offers

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[Offer]]:
        """
        Scrapes job offers from JustJoinIT website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
        Returns:
            List[Optional[Offer]]: A list of scraped offer inputs.
        """
        driver = get_driver()
        driver.get(url)

        data = self.get_content(driver)
        parsed_offers = self.parse_offers(data, max_offer_duration_days)

        print(f"Parsed {len(parsed_offers)} offers")
        return parsed_offers
