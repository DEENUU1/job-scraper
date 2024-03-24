from utils.get_current_date import get_current_date
from .url_exists import url_exist
from schemas.offer_schema import OfferInput
import gspread


def add_data_to_sheet(
        data: OfferInput,
        website: str,
        worksheet: gspread.Worksheet,
        url_column: int = 2,
) -> None:
    if not url_exist(worksheet, url_column, data.url):
        row_data = [
            data.title,
            data.url,
            website,
            str(get_current_date())
        ]
        worksheet.insert_row(row_data, index=2)
        print("Save data to Google Sheet")
    else:
        print("Data already exist")
