import gspread

from utils.get_config import get_config

sh_url = get_config()["url"]
gc = gspread.service_account(filename="credentials.json")


def get_worksheet() -> gspread.Worksheet:
    return gc.open_by_url(sh_url).sheet1
