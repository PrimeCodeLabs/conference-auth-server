from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.conferences.models import Conference, Speaker
from app.attendees.models import Attendee
from app.db.models import User as AuthUser

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.conferences.models import Conference, Speaker
from app.attendees.models import Attendee
from app.db.models import User as AuthUser

def seed_db():
    db: Session = SessionLocal()
    
    users = [
        {"username": "user1", "password": "password"},
        {"username": "user2", "password": "password"},
        {"username": "speaker1", "password": "password"},
        {"username": "speaker2", "password": "password"},
        {"username": "attendee1", "password": "password"},
        {"username": "attendee2", "password": "password"}
    ]
    
    conferences = [
        {"title": "Conference 1", "description": "Description 1"},
        {"title": "Conference 2", "description": "Description 2"}
    ]

    speakers = [
        {"name": "Speaker 1", "bio": "Bio 1", "username": "speaker1"},
        {"name": "Speaker 2", "bio": "Bio 2", "username": "speaker2"}
    ]

    attendees = [
        {"name": "Attendee 1", "email": "attendee1@example.com", "username": "attendee1", "conference_id": 1},
        {"name": "Attendee 2", "email": "attendee2@example.com", "username": "attendee2", "conference_id": 2}
    ]

    # Add users
    for user in users:
        db_user = db.query(AuthUser).filter(AuthUser.username == user["username"]).first()
        if not db_user:
            db_user = AuthUser(username=user["username"], hashed_password=user["password"])
            db.add(db_user)
    
    db.commit()  # Commit users to the database first

    # Add conferences
    for conference in conferences:
        db_conference = Conference(title=conference["title"], description=conference["description"])
        db.add(db_conference)
    
    db.commit()  # Commit conferences to the database

    # Add speakers
    for speaker in speakers:
        db_user = db.query(AuthUser).filter(AuthUser.username == speaker["username"]).first()
        if db_user:
            db_speaker = Speaker(name=speaker["name"], bio=speaker["bio"], user_id=db_user.id)
            db.add(db_speaker)
    
    db.commit()  # Commit speakers to the database

    # Add attendees and link them to conferences
    for attendee in attendees:
        db_user = db.query(AuthUser).filter(AuthUser.username == attendee["username"]).first()
        if db_user:
            db_attendee = db.query(Attendee).filter(Attendee.email == attendee["email"]).first()
            if not db_attendee:
                db_attendee = Attendee(name=attendee["name"], email=attendee["email"])
                db.add(db_attendee)
                db.commit()  # Commit the attendee to get its ID

            db_conference = db.query(Conference).filter(Conference.id == attendee["conference_id"]).first()
            if db_conference and db_attendee not in db_conference.attendees:
                db_conference.attendees.append(db_attendee)
    
    db.commit()  # Commit the relationships

    db.close()

if __name__ == "__main__":
    seed_db()
