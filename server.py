from utils.get_config import get_config

config = get_config()
export_type = config["export_type"]

if export_type != "db":
    raise Exception("Export type not supported, set export_type to 'db' in config.json to run server")

from fastapi import FastAPI, Request, Depends, Query
from config.database import engine
from models.offer import Offer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from service.offer_service import OfferService
from config.database import get_db
from typing import Optional
from enums.sort_by import OfferSortEnum
from schemas.offer_status import OfferStatusUpdate


Offer.metadata.create_all(bind=engine)

app = FastAPI(
    debug=True,  # Always set to True because this app works only in local mode
    title="Job scraper"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.post("/offer_status")
def update_check_status(data: OfferStatusUpdate, session: Session = Depends(get_db)):
    offer_service = OfferService(session)
    return offer_service.change_check_status(data.offer_id, data.status)


@app.get("/", response_class=HTMLResponse)
def get_all(
        request: Request,
        session: Session = Depends(get_db),
        page: int = Query(1),
        page_limit: int = Query(50),
        query: Optional[str] = Query(None),
        sort_by: str = Query("newest")
):

    offer_service = OfferService(session)

    offers = offer_service.get_all(
        page=page,
        page_limit=page_limit,
        query=query,
        sort_by=sort_by
    )

    return templates.TemplateResponse(
        request=request,
        name="get_all.html",
        context={
            "offers": offers
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
