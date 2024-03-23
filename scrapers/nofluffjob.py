from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from time import sleep


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


def click_get_more(driver) -> None:
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tw-btn.tw-btn-primary.tw-px-8.tw-block.tw-btn-xl"))
        )
        driver.execute_script("arguments[0].click();", consent_button)
    except Exception as e:
        print(e)


def click_country(driver) -> None:
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tw-btn.tw-btn-xl.tw-text-gray-30.mr-3.ng-star-inserted"))
        )
        consent_button.click()
    except Exception as e:
        print(e)


def scraper() -> None:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://nofluffjobs.com/pl/Python?criteria=seniority%3Dtrainee,junior&page=1&sort=newest")
    click_country(driver)

    data = []

    def scrape(driver) -> None:
        click_get_more(driver)
        a_elements = driver.find_elements(By.TAG_NAME, "a")
        for element in a_elements:
            data.append(element.get_attribute("outerHTML"))

    scroll_page_callback(driver, scrape)

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
                offer = {"url": url, "title": title.text}
                offers.append(offer)

    print(offers)
    print(len(offers))


