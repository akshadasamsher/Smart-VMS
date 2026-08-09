from sqlalchemy import Column, Integer, String, Float

from database import Base


class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    camera_id = Column(String, nullable=False)

    event_type = Column(String, nullable=False)

    timestamp = Column(Float, nullable=False)

    confidence = Column(Float, nullable=True)

    zone = Column(String, nullable=True)