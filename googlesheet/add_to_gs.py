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
    """
    Adds data to a Google Sheet if the URL does not already exist in the specified column.

    Args:
        data (OfferInput): The data to be added to the sheet.
        website (str): The website associated with the data.
        worksheet (gspread.Worksheet): The worksheet where the data will be added.
        url_column (int, optional): The column index where URLs are stored. Defaults to 2.

    Returns:
        None
    """
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
