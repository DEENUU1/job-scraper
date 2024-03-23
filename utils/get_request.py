import requests


def get_request(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except Exception as e:
        print(e)
        return None
