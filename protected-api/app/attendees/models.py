from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Attendee(Base):
    __tablename__ = "attendees"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
