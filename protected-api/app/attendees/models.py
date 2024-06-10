from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

conference_attendees = Table(
    'conference_attendees', Base.metadata,
    Column('conference_id', Integer, ForeignKey('conferences.id')),
    Column('attendee_id', Integer, ForeignKey('attendees.id')),
    extend_existing=True
)

class Attendee(Base):
    __tablename__ = "attendees"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    conferences = relationship("Conference", secondary=conference_attendees, back_populates="attendees")
