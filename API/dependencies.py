from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from passlib.context import CryptContext
import jwt
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session
from API.config import ALGORITHM, SECRET_KEY, SessionLocal
from API.crud import crud
from API.models import models
from API.schemas import schemas
import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    expired_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expiré, Veuillez vous reconnecter !",
        headers={"WWW-Authenticate": "Bearer"},
    )


    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expiration: datetime = payload.get("exp")

        if expiration:
            expiration_datetime = datetime.fromtimestamp(expiration, tz=timezone.utc)
            if datetime.now(timezone.utc) > expiration_datetime:
                raise expired_token_exception
    
        if username is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(username=username)


    except ExpiredSignatureError:
        # Gérer les erreurs d'expiration de signature
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré, Veuillez vous reconnecter !.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except JWTError:
            raise credentials_exception
    
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user





def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




def authenticate_user(db: Session, username: str, password: str) -> models.User:
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
