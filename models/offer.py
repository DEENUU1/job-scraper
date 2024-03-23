import uuid

from sqlalchemy import Column, UUID, String, Boolean, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from config.database import Base
from enums.status import StatusEnum


class Offer(Base):
    __tablename__ = "offers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    archived = Column(Boolean, default=False)
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False, default=StatusEnum.NEW)
    website_id = Column(UUID(as_uuid=True), ForeignKey('websites.id'), nullable=False)
    website = relationship("Website", back_populates="offers")
