from repository.website_repository import WebsiteRepository
from sqlalchemy.orm import Session
from schemas.website_schema import WebsiteInput, WebsiteOutput
from pydantic import UUID4

from typing import List


class WebsiteService:
    def __init__(self, session: Session) -> None:
        self.website_repository = WebsiteRepository(session)

    def create(self, website_input: WebsiteInput) -> WebsiteOutput:
        if self.website_repository.website_exists_by_url(website_input.url):
            raise ValueError("Website already exists")

        return self.website_repository.create(website_input)

    def get_all_websites(self) -> List[WebsiteOutput]:
        return self.website_repository.get_all_websites()

    def update_url(self, website_input: WebsiteInput) -> WebsiteOutput:
        if not self.website_repository.website_exists_by_url(website_input.url):
            raise ValueError("Website does not exist")

        website = self.website_repository.get_website_object_by_url(website_input.url)

        return self.website_repository.update_url(website, website_input.url)

    def delete_website(self, website_id: UUID4) -> None:
        if not self.website_repository.website_exists_by_url(website_id):
            raise ValueError("Website does not exist")

        website = self.website_repository.get_website_object_by_id(website_id)
        self.website_repository.delete(website)


