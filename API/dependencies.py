from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from passlib.context import CryptContext
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session
from config import ALGORITHM, SECRET_KEY, SessionLocal
from models import User
from schemas import TokenData, UserCreate, UserInDB
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





# ============================ Authentification ================================



def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()



def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserInDB:
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
        
        token_data = TokenData(username=username)


    except ExpiredSignatureError:
        # Gérer les erreurs d'expiration de signature
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré, Veuillez vous reconnecter !.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except JWTError:
            raise credentials_exception
    
    user = get_user(db, username=token_data.username)
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




def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



