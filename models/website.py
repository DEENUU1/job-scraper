import uuid

from sqlalchemy import Column, UUID, String

from config.database import Base


class Website(Base):
    __tablename__ = "website"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False)
