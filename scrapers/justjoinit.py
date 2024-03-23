from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def scraper() -> None:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://justjoin.it/all-locations/java/experience-level_junior")
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

    titles = []
    for d in data:
        soup = BeautifulSoup(d, "html.parser")
        title = soup.find("h2")
        url = soup.find("a")

        if title and url:
            title = title.text
            url = url.get("href")

            if url not in titles:
                titles.append(url)

    print(len(titles))