from sqlalchemy import Column, String, Integer, DateTime, func

from config.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    page = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
