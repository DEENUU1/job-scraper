import os

from config.database import engine
from models.offer import Offer
from tasks.run_all_scrapers import run_all_scraper
from utils.get_config import get_config

if not os.path.exists("urls_to_skip.txt"):
    with open("urls_to_skip.txt", "w") as f:
        f.write("")

config = get_config()

worksheet_url = config["url"]
# Get the list of websites from configuration
websites = config["websites"]
# Get the maximum offer duration from configuration
max_offer_duration_days = config["max_offer_duration_days"]
keywords_to_pass = config["keywords_to_pass"]
export_type = config["export_type"]

if export_type == "db":
    # Create the Offer table if it doesn't exist
    Offer.metadata.create_all(bind=engine)


def main() -> None:
    """
    Main function to run the web scraping tasks.

    Returns:
        None
    """

    run_all_scraper(
        websites,
        worksheet_url,
        export_type,
        max_offer_duration_days,
        keywords_to_pass
    )


if __name__ == '__main__':
    main()
