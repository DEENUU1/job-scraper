from googlesheet.init_gs import get_worksheet
from tasks.run_all_scrapers import run_all_scraper
from utils.get_config import get_config


def main() -> None:
    sh = get_worksheet()
    websites = get_config()["websites"]
    run_all_scraper(websites, sh)


if __name__ == '__main__':
    main()
