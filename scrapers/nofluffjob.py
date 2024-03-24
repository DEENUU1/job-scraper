from time import sleep
from typing import Optional, List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from schemas.offer_schema import OfferInput
from utils.get_driver import get_driver
from .abc.scraper_strategy import ScraperStrategy


class Nofluffjob(ScraperStrategy):
    """
    A class implementing the scraping strategy for Nofluffjob website.
    """

    @staticmethod
    def scroll_page_callback(driver, callback) -> None:
        """
        Scroll the webpage and execute a callback function repeatedly until certain conditions are met.

        Args:
            driver: Selenium WebDriver instance.
            callback: Callback function to execute after each scroll.
        """
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            consecutive_scrolls = 0

            while consecutive_scrolls < 3:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                sleep(3)
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    consecutive_scrolls += 1
                else:
                    consecutive_scrolls = 0

                last_height = new_height

                callback(driver)

        except Exception as e:
            print(e)

    @staticmethod
    def click_get_more(driver) -> None:
        """
        Click the "Get more" button on the webpage.

        Args:
            driver: Selenium WebDriver instance.
        """
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tw-btn.tw-btn-primary.tw-px-8.tw-block.tw-btn-xl"))
            )
            driver.execute_script("arguments[0].click();", consent_button)
        except Exception as e:
            print(e)

    @staticmethod
    def click_country(driver) -> None:
        """
        Click the country selection button on the webpage.

        Args:
            driver: Selenium WebDriver instance.
        """
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.tw-btn.tw-btn-xl.tw-text-gray-30.mr-3.ng-star-inserted"))
            )
            consent_button.click()
        except Exception as e:
            print(e)

    @staticmethod
    def parse_offers(data) -> List[Optional[OfferInput]]:
        """
        Parse job offers from HTML data.

        Args:
            data: List of HTML data.

        Returns:
            List[Optional[OfferInput]]: A list of parsed offer inputs.
        """
        offers = []
        unique_urls = []
        for d in data:
            soup = BeautifulSoup(d, "html.parser")
            target_url = soup.find("a", href=lambda href: href and "pl/job" in href)
            if target_url:
                url = target_url.get("href")
                title = target_url.find("h3")

                if title and url not in unique_urls:
                    unique_urls.append(url)

                    full_url = f"nofluffjobs.com{url}"
                    offers.append(OfferInput(title=title.text, url=full_url))

        return offers

    def scrape(self, url: str, max_offer_duration_days: Optional[int] = None) -> List[Optional[OfferInput]]:
        """
        Scrape job offers from Nofluffjob website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
        Returns:
            List[Optional[OfferInput]]: A list of scraped offer inputs.
        """
        print(f"Run Nofluffjob scraper")

        driver = get_driver()
        driver.get(url)
        self.click_country(driver)

        data = []

        def scrape_callback(driver) -> None:
            self.click_get_more(driver)
            a_elements = driver.find_elements(By.TAG_NAME, "a")
            for element in a_elements:
                data.append(element.get_attribute("outerHTML"))

        self.scroll_page_callback(driver, scrape_callback)

        parsed_offers = self.parse_offers(data)

        print(f"Scraped {len(parsed_offers)} offers")
        return parsed_offers
