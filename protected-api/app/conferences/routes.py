from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.conferences import crud, schemas
from app.db.database import get_db
from app.db.models import User 
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Conference)
def create_conference(conference: schemas.ConferenceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_conference(db=db, conference=conference)

@router.get("/{conference_id}", response_model=schemas.Conference)
def read_conference(conference_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_conference = crud.get_conference(db, conference_id=conference_id)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    return db_conference

@router.get("/", response_model=list[schemas.Conference])
def read_conferences(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    conferences = crud.get_conferences(db, skip=skip, limit=limit)
    return conferences

@router.post("/speakers/", response_model=schemas.Speaker)
def create_speaker(speaker: schemas.SpeakerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_speaker(db=db, speaker=speaker)

@router.get("/speakers/{speaker_id}", response_model=schemas.Speaker)
def read_speaker(speaker_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_speaker = crud.get_speaker(db, speaker_id=speaker_id)
    if db_speaker is None:
        raise HTTPException(status_code=404, detail="Speaker not found")
    return db_speaker

@router.get("/speakers/", response_model=List[schemas.Speaker])
def read_speakers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    speakers = crud.get_speakers(db, skip=skip, limit=limit)
    return speakers