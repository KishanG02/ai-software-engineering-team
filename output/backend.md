# FILE: requirements.txt

```bash
fastapi
uvicorn
sqlalchemy
psycopg2
python-dotenv
passlib
pydantic
python-jose
```

# FILE: .env.example

```makefile
DATABASE_URL="postgresql://user:password@localhost:5432/database"
SECRET_KEY="secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

# FILE: app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.core.config import settings
from app.routes.auth import auth_router
from app.routes.user import user_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"message": "Healthy"}

@app.on_event("shutdown")
def shutdown_event():
    engine.dispose()
```

# FILE: app/database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

# FILE: app/core/config.py

```python
from pydantic import BaseSettings
from python_dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

settings = Settings()
```

# FILE: app/core/security.py

```python
from passlib.context import CryptContext
from python_jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user
```

# FILE: app/models/user.py

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def __init__(self, email, hashed_password):
        self.email = email
        self.hashed_password = hashed_password
```

# FILE: app/schemas/user.py

```python
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
```

# FILE: app/routes/auth.py

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import verify_password, get_password_hash, create_access_token
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate

auth_router = APIRouter()

@auth_router.post("/register")
def register(user: UserCreate, db = Depends(get_db)):
    user_obj = User(email=user.email, hashed_password=get_password_hash(user.password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"message": "User created successfully"}

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

# FILE: app/routes/user.py

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import User

user_router = APIRouter()

@user_router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user), db = Depends(get_db)):
    return current_user
```

# FILE: Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

# FILE: docker-compose.yml

```yml
version: '3'

services:
  app:
    build: .
    environment:
      - DATABASE_URL=postgresql://user:password@localhost:5432/database
      - SECRET_KEY=secret_key
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    ports:
      - "8000:8000"
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

Please note that you need to replace the placeholders in the `.env.example` and `docker-compose.yml` files with your actual database credentials and secret key. Also, you need to create a `database` directory in the root of your project and add a `__init__.py` file to it to make it a package. 

You can run the application using `docker-compose up` and access it at `http://localhost:8000`. You can use a tool like `curl` or a REST client to test the API endpoints. 

Remember to install the required packages using `pip install -r requirements.txt` before building the Docker image. 

Also, please note that this is a basic example and you should consider security and other best practices when building a real-world application.