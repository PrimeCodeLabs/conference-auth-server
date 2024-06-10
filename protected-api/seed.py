# protected-api/seed.py
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.conferences.models import Conference, Speaker
from app.db.models import User as AuthUser

def seed_db():
    db: Session = SessionLocal()
    
    users = [
        {"username": "user1", "password": "password"},
        {"username": "user2", "password": "password"},
        {"username": "speaker1", "password": "password"},
        {"username": "speaker2", "password": "password"}
    ]
    
    conferences = [
        {"title": "Conference 1", "description": "Description 1"},
        {"title": "Conference 2", "description": "Description 2"}
    ]

    speakers = [
        {"name": "Speaker 1", "bio": "Bio 1", "username": "speaker1"},
        {"name": "Speaker 2", "bio": "Bio 2", "username": "speaker2"}
    ]
    
    for user in users:
        db_user = db.query(AuthUser).filter(AuthUser.username == user["username"]).first()
        if not db_user:
            db_user = AuthUser(username=user["username"], hashed_password=user["password"])
            db.add(db_user)
    
    for conference in conferences:
        db_conference = Conference(title=conference["title"], description=conference["description"])
        db.add(db_conference)
    
    for speaker in speakers:
        db_user = db.query(AuthUser).filter(AuthUser.username == speaker["username"]).first()
        db_speaker = Speaker(name=speaker["name"], bio=speaker["bio"], user=db_user)
        db.add(db_speaker)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_db()
