from fastapi import FastAPI
from app.db.database import engine, Base
from app.attendees.routes import router as attendees_router
from app.conferences.routes import router as conferences_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Protected API Server")

app.include_router(attendees_router, prefix="/attendees")
app.include_router(conferences_router, prefix="/conferences")


