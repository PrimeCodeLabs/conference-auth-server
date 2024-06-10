import os
from sqlalchemy.orm import Session
from app.db.database import engine
from app.db.models import Base, User
from app.utils.hashing import get_password_hash

# Initialize the database and create tables
Base.metadata.create_all(bind=engine)

# Create a new session
session = Session(bind=engine)

# Define the initial users
initial_users = [
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"},
    {"username": "admin", "password": "adminpass"},
]

# Add users to the database
for user_data in initial_users:
    existing_user = session.query(User).filter(User.username == user_data["username"]).first()
    if existing_user:
        print(f"User {user_data['username']} already exists.")
        continue
    hashed_password = get_password_hash(user_data["password"])
    user = User(username=user_data["username"], hashed_password=hashed_password)
    session.add(user)

# Commit the transaction and close the session
session.commit()
session.close()

print("Database seeded with initial users.")
