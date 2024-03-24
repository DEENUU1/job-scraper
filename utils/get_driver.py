from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    """
    Retrieves a WebDriver instance for Chrome browser.

    Returns:
        webdriver.Chrome: WebDriver instance for Chrome browser.
    """
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
