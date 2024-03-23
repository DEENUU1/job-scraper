from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def scraper() -> None:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


    offers = []
    base_url = "https://pl.indeed.com/praca?l=Zdu%C5%84ska+Wola%2C+%C5%82%C3%B3dzkie&radius=10&sort=date&vjk=adc0ec0fd20bd577"

    while True:
        driver.get(base_url)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        job_elements = soup.find_all("li", class_="css-5lfssm")

        for offer in job_elements:
            url = offer.find("a", class_="jcs-JobTitle")
            if url:
                title = url.find("span")

                d = {"url": url.get("href"), "title": title.text}
                print(d)
                offers.append(d)

        next_page_button = soup.find("a", {"data-testid": "pagination-page-next"})
        if not next_page_button:
            break

        if next_page_button:
            base_url = "https://pl.indeed.com" + next_page_button.get("href")

    print(offers)
    print(len(offers))