from sqlalchemy.orm import Session
from app.conferences import models, schemas

def get_conference(db: Session, conference_id: int):
    return db.query(models.Conference).filter(models.Conference.id == conference_id).first()

def get_conferences(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Conference).offset(skip).limit(limit).all()

def create_conference(db: Session, conference: schemas.ConferenceCreate):
    db_conference = models.Conference(name=conference.name, location=conference.location)
    db.add(db_conference)
    db.commit()
    db.refresh(db_conference)
    return db_conference
