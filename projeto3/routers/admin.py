from typing import Annotated
from fastapi import  Depends, HTTPException, Path
from sqlalchemy.orm import Session
import tables as tables
from tables import Todos
from models.todos import Todos_Model
from database import SessionLocal
from starlette import status
from fastapi import APIRouter, Path, Query, HTTPException
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

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

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependecy, db:db_dependecy):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Não autorizado")
    
    return db.query(Todos).all()

@router.delete("/todo/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def detele_todo(user: user_dependecy
                      , db: db_dependecy
                      , todo_id: int = Path(ge=1)):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Não autorizado")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
                                .first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="To Do não encontrado.")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

