from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_modal(driver) -> None:
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-name="_crazyPopUpNoButton"]'))
        )
        consent_button.click()
    except Exception as e:
        print(e)