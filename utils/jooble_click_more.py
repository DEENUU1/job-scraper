from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_see_more(driver) -> None:
    try:
        consent_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "VMdYVt"))
        )
        consent_button.click()
    except Exception as e:
        print(e)