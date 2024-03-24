from scrapers.bulldogjob import BulldogJob
from scrapers.indeed import Indeed
from scrapers.itpracujpl import ITPracujPL
from scrapers.jooble import Jooble
from scrapers.justjoinit import JustJoinIT
from scrapers.nofluffjob import Nofluffjob
from scrapers.olx import OLX
from scrapers.pracujpl import PracujPL
from scrapers.theprotocol import TheProtocol
from scrapers.useme import Useme


def url_to_scraper(url: str):
    """
    Maps a URL to the corresponding scraper class and website name.

    Args:
        url (str): The URL to map to a scraper.

    Returns:
        tuple: A tuple containing the scraper class and the website name.
               If the URL does not match any supported websites, returns (None, None).
    """
    if "pracuj.pl" in url and "it.pracuj.pl" not in url:
        return PracujPL(), "PracujPL"
    if "bulldogjob" in url:
        return BulldogJob(), "Bulldogjob"
    if "indeed" in url:
        return Indeed(), "Indeed"
    if "jooble" in url:
        return Jooble(), "Jooble"
    if "justjoin" in url:
        return JustJoinIT(), "JustJoinIT"
    if "nofluffjobs" in url:
        return Nofluffjob(), "Nofluffjob"
    if "theprotocol" in url:
        return TheProtocol(), "TheProtocol"
    if "it.pracuj.pl" in url:
        return ITPracujPL(), "ITPracujPL"
    if "useme" in url:
        return Useme(), "Useme"
    if "olx" in url:
        return OLX(), "OLX"

    return None, None
