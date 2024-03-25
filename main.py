from googlesheet.init_gs import get_worksheet
from tasks.run_all_scrapers import run_all_scraper
from utils.get_config import get_config
import os


if not os.path.exists("urls_to_skip.txt"):
    with open("urls_to_skip.txt", "w") as f:
        f.write("")


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
    keywords_to_pass = config["keywords_to_pass"]

    # Run all scrapers for the given websites and add data to the worksheet
    run_all_scraper(websites, sh, max_offer_duration_days, keywords_to_pass)


if __name__ == '__main__':
    main()
