from pydantic import BaseModel
from typing import List

class SpeakerBase(BaseModel):
    name: str
    bio: str

class SpeakerCreate(SpeakerBase):
    pass

class Speaker(SpeakerBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class ConferenceBase(BaseModel):
    title: str
    description: str

class ConferenceCreate(ConferenceBase):
    pass

class Conference(ConferenceBase):
    id: int
    speakers: List[Speaker] = []

    class Config:
        orm_mode = True
