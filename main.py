from googlesheet.init_gs import get_worksheet
from tasks.run_all_scrapers import run_all_scraper
from utils.get_config import get_config


def main() -> None:
    """
    Main function to run the web scraping tasks.

    Returns:
        None
    """
    sh = get_worksheet()  # Get the Google Sheet worksheet
    websites = get_config()["websites"]  # Get the list of websites from configuration
    run_all_scraper(websites, sh)  # Run all scrapers for the given websites and add data to the worksheet


if __name__ == '__main__':
    main()
