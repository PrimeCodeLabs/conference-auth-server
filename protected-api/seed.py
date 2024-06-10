import os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.attendees import models as attendees_models
from app.conferences import models as conferences_models

# Create the database tables
Base.metadata.create_all(bind=engine)

# Sample data
attendees = [
    {"name": "Alice Smith", "email": "alice@example.com"},
    {"name": "Bob Jones", "email": "bob@example.com"},
    {"name": "Charlie Brown", "email": "charlie@example.com"}
]

conferences = [
    {"name": "Tech Conference 2024", "location": "San Francisco"},
    {"name": "Health Conference 2024", "location": "New York"}
]

def seed_db():
    db: Session = SessionLocal()
    try:
        for attendee in attendees:
            db_attendee = attendees_models.Attendee(name=attendee["name"], email=attendee["email"])
            db.add(db_attendee)
        
        for conference in conferences:
            db_conference = conferences_models.Conference(name=conference["name"], location=conference["location"])
            db.add(db_conference)
        
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
    print("Database seeded with initial data.")
