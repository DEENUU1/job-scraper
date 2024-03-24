import json


def get_config():
    """
    Retrieves configuration settings from a JSON file named "config.json".

    Returns:
        dict: The configuration settings loaded from the JSON file.
    """
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    return config
