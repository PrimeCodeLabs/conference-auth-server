from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

# Association table for many-to-many relationship between conferences and speakers
conference_speakers = Table(
    'conference_speakers', Base.metadata,
    Column('conference_id', Integer, ForeignKey('conferences.id')),
    Column('speaker_id', Integer, ForeignKey('speakers.id')),
    extend_existing=True
)

class Conference(Base):
    __tablename__ = "conferences"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False, default="Untitled Conference")
    description = Column(String,  nullable=True, default="")
    speakers = relationship("Speaker", secondary=conference_speakers, back_populates="conferences")
    attendees = relationship("Attendee", secondary="conference_attendees", back_populates="conferences")

class Speaker(Base):
    __tablename__ = "speakers"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")
    conferences = relationship("Conference", secondary=conference_speakers, back_populates="speakers")
