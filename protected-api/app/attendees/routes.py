from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.attendees import crud, schemas
from app.db.database import get_db
from app.db.models import User 
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Attendee)
def create_attendee(attendee: schemas.AttendeeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_attendee(db=db, attendee=attendee)

@router.get("/{attendee_id}", response_model=schemas.Attendee)
def read_attendee(attendee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_attendee = crud.get_attendee(db, attendee_id=attendee_id)
    if db_attendee is None:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return db_attendee

@router.get("/", response_model=list[schemas.Attendee])
def read_attendees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    attendees = crud.get_attendees(db, skip=skip, limit=limit)
    return attendees
