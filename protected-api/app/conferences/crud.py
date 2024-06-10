from sqlalchemy.orm import Session
from app.conferences.models import Conference, Speaker
from app.conferences.schemas import ConferenceCreate, SpeakerCreate

def get_conference(db: Session, conference_id: int):
    return db.query(Conference).filter(Conference.id == conference_id).first()

def get_conferences(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Conference).offset(skip).limit(limit).all()

def create_conference(db: Session, conference: ConferenceCreate):
    db_conference = Conference(title=conference.title, description=conference.description)
    db.add(db_conference)
    db.commit()
    db.refresh(db_conference)
    return db_conference

def get_speaker(db: Session, speaker_id: int):
    return db.query(Speaker).filter(Speaker.id == speaker_id).first()

def get_speakers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Speaker).offset(skip).limit(limit).all()

def create_speaker(db: Session, speaker: SpeakerCreate, user_id: int):
    db_speaker = Speaker(**speaker.dict(), user_id=user_id)
    db.add(db_speaker)
    db.commit()
    db.refresh(db_speaker)
    return db_speaker
