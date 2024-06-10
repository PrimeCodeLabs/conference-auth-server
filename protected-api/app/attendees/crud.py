from sqlalchemy.orm import Session
from app.attendees import models, schemas

def get_attendee(db: Session, attendee_id: int):
    return db.query(models.Attendee).filter(models.Attendee.id == attendee_id).first()

def get_attendees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Attendee).offset(skip).limit(limit).all()

def create_attendee(db: Session, attendee: schemas.AttendeeCreate):
    db_attendee = models.Attendee(name=attendee.name, email=attendee.email)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee
