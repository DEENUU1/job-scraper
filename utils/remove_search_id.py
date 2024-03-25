
def remove_search_id_from_url(url: str) -> str:
    url_parts = url.split("?")
    return url_parts[0]
