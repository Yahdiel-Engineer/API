from typing import Optional
from pydantic import BaseModel





class IrProperty(BaseModel):
    res_id: str
    value_float: float


class ProductTemplate(BaseModel):
    name: str
    categ_id: int
    list_price: float
    categ_name: str
    quantity: int



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

    class Config:
        orm_mode = True



class UserInDB(User):
    hashed_password: str



# Modèle Pydantic pour la création d'utilisateur
class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str




class Config:
    orm_mode = True

