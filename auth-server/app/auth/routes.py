import base64
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import timedelta
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from urllib.parse import urlencode
from hashlib import sha256
from app.db import models, database
from app.auth.schemas import Token, UserCreate, UserLogin
from app.utils.token import create_access_token
from app.utils.hashing import get_password_hash, verify_password
from app.core.config import settings

router = APIRouter()

logging.basicConfig(level=logging.INFO)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/authorize")
async def authorize(request: Request, response_type: str, client_id: str, redirect_uri: str, scope: str, state: str, code_challenge: str, code_challenge_method: str, db: Session = Depends(get_db)):
    return HTMLResponse(content=f"""
    <html>
        <body>
            <form action="/auth/authorize_confirm" method="post">
                <input type="hidden" name="response_type" value="{response_type}">
                <input type="hidden" name="client_id" value="{client_id}">
                <input type="hidden" name="redirect_uri" value="{redirect_uri}">
                <input type="hidden" name="scope" value="{scope}">
                <input type="hidden" name="state" value="{state}">
                <input type="hidden" name="code_challenge" value="{code_challenge}">
                <input type="hidden" name="code_challenge_method" value="{code_challenge_method}">
                <label for="username">Username:</label>
                <input type="text" name="username">
                <label for="password">Password:</label>
                <input type="password" name="password">
                <button type="submit">Authorize</button>
            </form>
        </body>
    </html>
    """)

@router.post("/authorize_confirm")
async def authorize_confirm(response_type: str = Form(...), client_id: str = Form(...), redirect_uri: str = Form(...), scope: str = Form(...), state: str = Form(...), code_challenge: str = Form(...), code_challenge_method: str = Form(...), username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Generate authorization code
    authorization_code = jwt.encode({"username": username, "code_challenge": code_challenge}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Redirect to the client with the authorization code
    query_params = urlencode({"code": authorization_code, "state": state})
    return RedirectResponse(f"{redirect_uri}?{query_params}")

@router.post("/token")
async def token(grant_type: str = Form(...), code: str = Form(None), redirect_uri: str = Form(None), client_id: str = Form(None), code_verifier: str = Form(None), db: Session = Depends(get_db)):
    if grant_type != "authorization_code":
        logging.error("Unsupported grant type")
        raise HTTPException(status_code=400, detail="Unsupported grant type")

    try:
        payload = jwt.decode(code, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as e:
        logging.error(f"JWT Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid authorization code")

    code_challenge = payload.get("code_challenge")
    expected_code_challenge = base64.urlsafe_b64encode(sha256(code_verifier.encode()).digest()).rstrip(b'=').decode()
    if code_challenge != expected_code_challenge:
        logging.error("Invalid code verifier")
        raise HTTPException(status_code=400, detail="Invalid code verifier")

    username = payload.get("username")
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        logging.error("User not found")
        raise HTTPException(status_code=400, detail="User not found")

    # Generate access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "expires_in": access_token_expires.total_seconds()}
