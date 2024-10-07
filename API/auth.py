from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from API.config import ACCESS_TOKEN_EXPIRE_MINUTES
from API.crud import create_user
from API.models import User
from API.schemas import Token, UserCreate, UserInDB  
from dependencies import create_access_token, get_current_user, get_db, authenticate_user
import sys
import os

# Ajouter le répertoire parent au chemin d'importation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'API')))







auth = APIRouter()

















@auth.post("/utilisateur/", response_model=UserInDB)
def créer_un_utilisateur(
    username: str = Form(...),
    password: str = Form(...),
    email: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le nom d'utilisateur et le mot de passe sont requis")

    user = UserCreate(
        username=username,
        email=email,
        full_name=full_name,
        password=password,
    )
    
    try:
        created_user = create_user(db, user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))












@auth.post("/token", response_model=Token)
def authentification_pour_un_jeton_d_accès(
      username: str = Form(...),
      password: str = Form(...),
      db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")











@auth.get("/utilisateur/utilisateur actuel/", response_model=User)
def voir_utilisateur_actuel(current_user: UserInDB = Depends(get_current_user)):
    return current_user


 