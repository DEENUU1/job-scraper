import gspread


def url_exist(worksheet: gspread.Worksheet, url_column: int, url_value: str):
    try:
        cell = worksheet.find(url_value, in_column=url_column)
        if cell:
            return True
        return False
    except:
        return False
