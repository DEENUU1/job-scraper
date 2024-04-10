from utils.get_config import get_config

config = get_config()
export_type = config["export_type"]

if export_type != "db":
    raise Exception("Export type not supported, set export_type to 'db' in config.json to run server")

from fastapi import FastAPI
from config.database import engine
from models.offer import Offer


Offer.metadata.create_all(bind=engine)


app = FastAPI(
    debug=True,  # Always set to True because this app works only in local mode
    title="Job scraper"
)



