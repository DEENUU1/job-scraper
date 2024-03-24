import requests


def get_request(url: str):
    """
    Sends a GET request to the specified URL and returns the response.

    Args:
        url (str): The URL to send the request to.

    Returns:
        requests.Response or None: The response object if successful, None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except Exception as e:
        print(e)
        return None
