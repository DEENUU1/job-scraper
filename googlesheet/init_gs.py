import gspread
from utils.get_config import get_config


def get_worksheet() -> gspread.Worksheet:
    """
    Retrieves a worksheet from a Google Sheets document based on the provided URL.

    Returns:
        gspread.Worksheet: The worksheet retrieved from the Google Sheets document.
    """
    sh_url = get_config()["url"]  # Retrieve the URL from the configuration
    gc = gspread.service_account(filename="credentials.json")  # Authenticate using service account credentials
    return gc.open_by_url(sh_url).sheet1  # Open the Google Sheets document and retrieve the first worksheet
