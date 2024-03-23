import uuid

from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import relationship

from config.database import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False, unique=True)
    offers = relationship("Offer", back_populates="website")
