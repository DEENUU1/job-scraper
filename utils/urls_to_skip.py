
def get_urls_to_skip():
    with open("urls_to_skip.txt", "r", encoding="utf-8") as file:
        result = file.read().splitlines()
        return result
