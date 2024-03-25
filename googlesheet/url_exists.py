import gspread


def url_exist(worksheet: gspread.Worksheet, url_column: int, url_value: str) -> bool:
    """
    Checks if a given URL value exists in the specified column of a worksheet.

    Args:
        worksheet (gspread.Worksheet): The worksheet to search in.
        url_column (int): The column index where URLs are stored.
        url_value (str): The URL value to search for.

    Returns:
        bool: True if the URL exists in the specified column, False otherwise.
    """
    try:
        cell = worksheet.find(url_value, in_column=url_column)
        if cell:
            return True
        return False
    except:
        return False