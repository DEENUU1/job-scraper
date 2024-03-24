from googlesheet.init_gs import get_worksheet
from tasks.run_all_scrapers import run_all_scraper
from utils.get_config import get_config


def main() -> None:
    """
    Main function to run the web scraping tasks.

    Returns:
        None
    """
    config = get_config()

    sh = get_worksheet()  # Get the Google Sheet worksheet
    websites = config["websites"]  # Get the list of websites from configuration
    max_offer_duration_days = config["max_offer_duration_days"]  # Get the maximum offer duration from configuration

    # Run all scrapers for the given websites and add data to the worksheet
    run_all_scraper(websites, sh, max_offer_duration_days)


if __name__ == '__main__':
    main()
