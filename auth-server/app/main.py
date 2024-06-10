from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.db.database import engine, Base
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authorization Server")

app.include_router(auth_router, prefix="/auth")

