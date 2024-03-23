from typing import List, Type
from pydantic import UUID4
from sqlalchemy.orm import Session
from models.website import Website
from schemas.website_schema import WebsiteInput, WebsiteOutput


class WebsiteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, website_input: WebsiteInput) -> WebsiteOutput:
        website = Website(**website_input.dict())
        self.session.add(website)
        self.session.commit()
        self.session.refresh(website)
        return WebsiteOutput(**website.__dict__)

    def get_all_websites(self) -> List[WebsiteOutput]:
        websites = self.session.query(Website).all()
        return [WebsiteOutput(**website.__dict__) for website in websites]

    def website_exists_by_url(self, url: str) -> bool:
        website = self.session.query(Website).filter_by(url=url).first()
        return bool(website)

    def get_website_object_by_url(self, url: str) -> Type[Website]:
        return self.session.query(Website).filter_by(url=url).first()

    def get_website_object_by_id(self, website_id: UUID4) -> Type[Website]:
        return self.session.query(Website).filter_by(id=website_id).first()

    def update_url(self, website: Type[Website], url: str) -> WebsiteOutput:
        website.url = url
        self.session.commit()
        self.session.refresh(website)
        return WebsiteOutput(**website.__dict__)

    def delete(self, website: Type[Website]) -> bool:
        self.session.delete(website)
        self.session.commit()
        return True

