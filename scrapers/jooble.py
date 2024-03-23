import requests
from bs4 import BeautifulSoup


def scraper() -> None:
    base_url = "https://pl.jooble.org/SearchResult?p=1000&rgns=Zdu%C5%84ska%20Wola%2C%20%C5%81%C3%B3dzkie"
    offers = []

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    elements = soup.find_all("div", class_="MhjGza")
    for element in elements:
        a_element = element.find("a", class_="_8w9Ce2")

        if a_element:
            title = a_element.text
            url = a_element.get("href")
            offers.append({"url": url, "title": title})

    print(len(offers))
