from fastapi import APIRouter, Depends
from models.users_model import User_Model
from tables import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

#Abre e fecha conexao
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Injecao de depencia que fala que é necessário fazer algo antes de executar o codigo
#No caso depende da funcao get_db.
db_dependecy = Annotated[Session, Depends(get_db)]

def autenticate_user(username: str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

@router.post("/auth/add", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: User_Model, 
                      db: db_dependecy):
    create_user_model = Users(
        email = user_request.email,
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        role = user_request.role,
        hashed_password = bcrypt_context.hash(user_request.password),
        is_activate = True
    )

    db.add(create_user_model)
    db.commit()

@router.post("/token")
async def login_for_acess_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependecy):
    # return form_data.username
    user = autenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed Authentication"
    return "Sucess Authentication"
