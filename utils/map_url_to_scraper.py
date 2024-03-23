from scrapers.bulldogjob import BulldogJob
from scrapers.indeed import Indeed
from scrapers.jooble import Jooble
from scrapers.justjoinit import JustJoinIT
from scrapers.nofluffjob import Nofluffjob
from scrapers.theprotocol import TheProtocol
from scrapers.pracujpl import PracujPL
from scrapers.useme import Useme
from scrapers.olx import OLX


def url_to_scraper(url: str):

    if "bulldogjob" in url:
        return BulldogJob()
    if "indeed" in url:
        return Indeed()
    if "jooble" in url:
        return Jooble()
    if "justjoin" in url:
        return JustJoinIT()
    if "nofluffjobs" in url:
        return Nofluffjob()
    if "theprotocol" in url:
        return TheProtocol()
    if "pracuj.pl" in url:
        return PracujPL()
    if "useme" in url:
        return Useme()
    if "olx" in url:
        return OLX()

    return None
