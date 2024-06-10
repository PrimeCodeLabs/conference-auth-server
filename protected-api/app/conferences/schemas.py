from pydantic import BaseModel

class ConferenceCreate(BaseModel):
    name: str
    location: str

class Conference(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        from_attributes = True 
