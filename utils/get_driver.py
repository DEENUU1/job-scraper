from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


def get_driver() -> WebDriver:
    """
    Get a Chrome WebDriver instance.

    Returns:
        WebDriver: Chrome WebDriver instance.
    """
    return webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        )
    )