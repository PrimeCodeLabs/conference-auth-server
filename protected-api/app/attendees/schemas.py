from pydantic import BaseModel

class AttendeeCreate(BaseModel):
    name: str
    email: str

class Attendee(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True 
