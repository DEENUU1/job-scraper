from typing import Optional, List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from schemas.offer import Offer
from .pracujpl_base import PracujPlBase


class PracujPL(PracujPlBase):
    """
    A class implementing the scraping strategy for PracujPL website.
    """

    def parse_data(self, content: str) -> List[Optional[Offer]]:
        """
        Parse job offer data from HTML content.

        Args:
            content (str): The HTML content to parse.

        Returns:
            List[Optional[Offer]]: A list of parsed offer inputs.
        """
        parsed_offers = []
        soup = BeautifulSoup(content, "html.parser")
        offers = soup.find_all("div", class_="tiles_c1k2agp8")
        print(f"Found {len(offers)} offers")

        for offer in offers:
            title = offer.find("h2")
            url = offer.find("a", class_="core_n194fgoq")
            if title and url:
                processed_url = self.remove_search_id(url.get("href"))

                parsed_offers.append(Offer(title=title.text, url=processed_url))

        print(f"Parsed {len(parsed_offers)} offers")
        return parsed_offers

    @staticmethod
    def close_modal(driver) -> None:
        """
        Close any modal that may appear on the page.

        Args:
            driver: The Selenium WebDriver instance.
        """
        try:
            modal = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "core_ig18o8w"))
            )
            modal.click()
        except Exception as e:
            print(e)

    def get_page_content(self, driver, base_url: str) -> Optional[str]:
        driver.get(base_url)
        self.close_modal(driver)
        page_content = driver.page_source
        if not page_content:
            return None

        print(f"Successfully visited: {base_url}")
        return page_content
