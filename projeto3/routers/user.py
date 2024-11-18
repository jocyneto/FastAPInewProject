from typing import Annotated
from fastapi import  Depends, HTTPException, Path
from sqlalchemy.orm import Session
import tables as tables
from database import SessionLocal
from starlette import status
from fastapi import APIRouter, Path, Query, HTTPException
from .auth import get_current_user
from passlib.context import CryptContext
from tables import Users
from models.password_verification import PasswordVerification

router = APIRouter(prefix="/user", tags=["user"])

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
user_dependecy = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')




@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_logged(user: user_dependecy, 
                          db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=401, detail="Não autorizado")
    
    usuario_logado = db.query(Users).filter(Users.id == user.get("id")).first()

    return usuario_logado

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_password_user(user: user_dependecy, 
                               db: db_dependecy, 
                               user_verification: PasswordVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Não autorizado para fazer operacao")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Não autorizado")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
