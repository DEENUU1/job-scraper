def theprotocol_remove_search_id(url: str) -> str:
    url_parts = url.split("?")
    return url_parts[0]
