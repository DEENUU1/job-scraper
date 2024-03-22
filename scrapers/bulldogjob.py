import requests
from bs4 import BeautifulSoup


def scraper() -> None:
    page_num = 1

    offers = []

    while True:
        base_url = f"https://bulldogjob.pl/companies/jobs/s/order,published,desc/page,{page_num}"

        response = requests.get(base_url)

        soup = BeautifulSoup(response.text, "html.parser")

        job_offers = soup.find_all("a", class_="JobListItem_item__M79JI")

        if not job_offers:
            break

        if job_offers:
            page_num += 1

        for offer in job_offers:
            title = offer.find("h3")

            if title:
                print(title.text)
                offers.append({"title": title.text})
