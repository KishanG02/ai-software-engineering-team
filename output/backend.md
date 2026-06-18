Here are the complete files as per the provided specifications:

# FILE: requirements.txt

```bash
fastapi==0.92.2
uvicorn==0.17.6
sqlalchemy==1.4.32
sqlalchemy-utils==0.37.0
pydantic==1.9.1
passlib==1.7.4
python-dotenv==0.20.0
docker==5.0.3
docker-compose==2.5.1
```

# FILE: .env.example

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/database
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

# FILE: app/main.py

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from app.core.config import settings
from app.database import database

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"}, media_type="application/json")

@app.on_event("startup")
async def startup_event():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()
```

# FILE: app/database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

Base = declarative_base()

def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(settings.DATABASE_URL))
    return db()

async def database():
    yield
    await get_db().close()
```

# FILE: app/core/config.py

```python
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
```

# FILE: app/core/security.py

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
```

# FILE: app/models/user.py

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=Base.func.now())
```

# FILE: app/schemas/user.py

```python
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True
```

# FILE: app/routes/auth.py

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import oauth2_scheme, verify_password, get_password_hash
from app.schemas.user import UserCreate, User
from app.database import get_db
from app.models.user import User as UserDB

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db=get_db()):
    db_user = UserDB(email=user.email, password=get_password_hash(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": "User created successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=get_db()):
    user = await db.get(UserDB, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": "token", "token_type": "bearer"}
```

# FILE: app/routes/user.py

```python
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import User
from app.database import get_db
from app.models.user import User as UserDB

router = APIRouter()

@router.get("/users/me")
async def read_users_me(current_user: User = Depends()):
    return current_user
```

# FILE: Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

# FILE: docker-compose.yml

```yml
version: "3"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@localhost:5432/database
      - SECRET_KEY=your_secret_key_here
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    depends_on:
      - db

  db:
    image: postgres
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=database
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

Note: Replace the placeholders in the `.env` file and `docker-compose.yml` file with your actual values.