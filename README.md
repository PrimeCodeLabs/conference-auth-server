# Conference Auth Server

## Overview

This project is a conference authentication server using FastAPI, PostgreSQL, and Docker. It includes two main services:
- `auth-server`: Handles user authentication and authorization.
- `protected-api`: Provides protected endpoints for conference attendees and conferences.

## Features

- **OAuth2 Authorization Code Grant with PKCE**: This project implements the Authorization Code Grant with Proof Key for Code Exchange (PKCE) for secure user authentication.

## Project Structure

```plaintext
.
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── auth-server
│   ├── Dockerfile
│   ├── __init__.py
│   ├── app
│   │   ├── auth
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── main.py
│   │   └── utils
│   │       ├── hashing.py
│   │       └── token.py
│   ├── requirements.txt
│   └── seed.py
├── docker-compose.yml
├── migrate
│   ├── Dockerfile
│   └── alembic
│       └── requirements.txt
├── protected-api
│   ├── Dockerfile
│   ├── app
│   │   ├── attendees
│   │   │   ├── crud.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── conferences
│   │   │   ├── crud.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   └── main.py
│   ├── requirements.txt
│   └── seed.py
└── scripts
    └── generate_code.py
```

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/PrimeCodeLabs/conference-auth-server.git
    cd conference-auth-server
    ```

2. Create a `.env` file in both `auth-server` and `protected-api` directories with the following content:
    ```dotenv
    DATABASE_URL=postgresql://user:password@db:5432/conference_db
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

3. Build and start the Docker containers:
    ```sh
    docker-compose up --build
    ```

## End-to-End Auth Process Diagram
```plaintext
                +-------------+                              +----------------+
                |             |                              |                |
                |   Client    |                              |   Auth Server  |
                |             |                              |                |
                +-------------+                              +----------------+
                     |                                             |
                     | Generate Code Verifier and Code Challenge   |
                     |--------------------------------------------> |
                     |                                             |
                     |     Authorization Request (code_challenge)  |
                     |--------------------------------------------> |
                     |                                             |
                     |                                             |
                     |          Authorization Response (code)      |
                     | <------------------------------------------ |
                     |                                             |
                     |                                             |
                     |     Token Request (code_verifier)           |
                     |--------------------------------------------> |
                     |                                             |
                     |                                             |
                     |            Token Response (token)           |
                     | <------------------------------------------ |
                     |                                             |
                +-------------+                              +----------------+
                |             |                              |                |
                | Protected API|                              |  Resource Server|
                |             |                              |                |
                +-------------+                              +----------------+
                     |                                             |
                     |  Access Protected Resource with Token       |
                     |--------------------------------------------> |
                     |                                             |
                     |   Resource Response                         |
                     | <------------------------------------------ |
```
## Example Implementation

### Step 1: Generate Code Verifier and Code Challenge

The code to generate `code_verifier` and `code_challenge` is inside the `scripts` directory.

```python
import hashlib
import base64
import os

def generate_code_verifier():
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode('utf-8')

code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

print("Code Verifier:", code_verifier)
print("Code Challenge:", code_challenge)
```

### Step 2: Authorization Request

The client sends the user to the authorization endpoint:

```bash
http://localhost:8000/auth/authorize?response_type=code&client_id=testclient&redirect_uri=http://localhost:8000/auth/callback&scope=openid&state=state123&code_challenge=<code_challenge>&code_challenge_method=S256
```

### Step 3: Authorization Endpoint Implementation

**In `auth-server/app/auth/routes.py`:**

```python
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

    authorization_code = jwt.encode({"username": username, "code_challenge": code_challenge}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    query_params = urlencode({"code": authorization_code, "state": state})
    return RedirectResponse(f"{redirect_uri}?{query_params}")
```

### Step 4: Token Endpoint Implementation

**In `auth-server/app/auth/routes.py`:**

```python
@router.post("/token")
async def token(grant_type: str = Form(...), code: str = Form(None), redirect_uri: str = Form(None), client_id: str = Form(None), code_verifier: str = Form(None), db: Session = Depends(get_db)):
    if grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="Unsupported grant type")

    try:
        payload = jwt.decode(code, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid authorization code")

    code_challenge = payload.get("code_challenge")
    expected_code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b'=').decode()
    if code_challenge != expected_code_challenge:
        raise HTTPException(status_code=400, detail="Invalid code verifier")

    username = payload.get("username")
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "expires_in": access_token_expires.total_seconds()}
```

### Testing the Full Flow

#### Generate Code Verifier and Code Challenge

Run the Python script to generate the `code_verifier` and `code_challenge`.

```python
import hashlib
import base64
import os

def generate_code_verifier():
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode('utf-8')

code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

print

("Code Verifier:", code_verifier)
print("Code Challenge:", code_challenge)
```

#### Register a New User

```sh
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "password": "testpassword"
}'
```

#### Authorize the User

Open a browser and navigate to:

```bash
http://localhost:8000/auth/authorize?response_type=code&client_id=testclient&redirect_uri=http://localhost:8000/auth/callback&scope=openid&state=state123&code_challenge=<code_challenge>&code_challenge_method=S256
```

#### Exchange Authorization Code for an Access Token

```sh
curl -X POST "http://localhost:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d 'grant_type=authorization_code&code=<authorization_code>&redirect_uri=http://localhost:8000/auth/callback&client_id=testclient&code_verifier=<code_verifier>'
```
Replace `<authorization_code>` and `<code_verifier>` with the actual values.

#### Access a Protected Route

```sh
curl -X GET "http://localhost:8000/attendees" -H "Authorization: Bearer <your_access_token>"
```
Replace `<your_access_token>` with the access token obtained from the previous step.

## Running Migrations

To run database migrations, use the following command:
```sh
docker-compose run migrate alembic upgrade head
```

## Seeding the Database

To seed the database with initial data, use the following command:
```sh
docker-compose run protected-api alembic upgrade head
docker-compose run protected-api python /app/protected-api/app/seed.py
```

## License

This project is licensed under the MIT License.