import requests


def scraper() -> None:
    base_url = "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=4&region_id=7&city_id=41415&sort_by=created_at%3Adesc&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5"
    offers = []
    while True:
        response = requests.get(base_url)
        data = response.json()

        for d in data["data"]:
            offers.append({"title": d["title"], "url": d["url"]})

        next_page_element = data.get("links").get("next")

        if not next_page_element:
            break

        if next_page_element:
            base_url = next_page_element.get("href")

    print(len(offers))