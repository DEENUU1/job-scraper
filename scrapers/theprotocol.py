import requests
from bs4 import BeautifulSoup


def scraper() -> None:
    base_url = "https://theprotocol.it/filtry/python;t/trainee,assistant,junior;p/praca/junior-python-developer-gdynia,oferta,84250000-d6d1-1a10-17fd-08dc41b13901?s=133835811&searchId=da0a9bc0-e89a-11ee-b1b6-150d11c0d08b&sort=date"
    page_numer = 1
    url = base_url + "&pageNumber=" + str(page_numer)

    offers = []
    while True:
        page_content = requests.get(url).text
        soup = BeautifulSoup(page_content, 'html.parser')

        job_offers = soup.find_all("div", class_="mainWrapper_m12z7gd6")

        if job_offers:
            page_numer += 1
            url = base_url + "&pageNumber=" + str(page_numer)

        if not job_offers:
            break

        for offer in job_offers:
            title = offer.find("h2", class_="titleText_te02th1")
            offer_url = offer.get('href')

            if title:
                title = title.text
                offers.append({"url": offer_url, "title": title})

        print(page_numer)

    print(len(offers))
