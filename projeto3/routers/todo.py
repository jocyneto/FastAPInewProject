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

router = APIRouter()

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

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependecy,db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autorizado")
    retorno = db.query(Todos).filter(Todos.user_id == user.get("id")).all()
    teste = db.query(Todos).all()
    return retorno

# @router.get("/", status_code=status.HTTP_200_OK)
# async def read_all(db: db_dependecy):
#     retorno = db.query(Todos).all()
#     return retorno

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependecy
                         ,db: db_dependecy
                         ,todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario nao encontrado.")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
                                .filter(Todos.user_id == user.get("id"))\
                                .first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="To do not found!")

@router.post("/todos/add/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependecy,
                      db: db_dependecy, 
                      todo_request: Todos_Model):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario não autorizado.")
    
    todo_model = Todos(**todo_request.model_dump(), user_id = user.get("id"))
    
    db.add(todo_model)
    db.commit()

@router.put("/todos/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependecy
                      ,db: db_dependecy
                      ,todo_request: Todos_Model
                      ,todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario não autorizado.")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
                                .filter(Todos.user_id == user.get("id"))\
                                .first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="To do not found!")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependecy
                     ,db: db_dependecy
                     ,todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario não autorizado.")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
                                .filter(Todos.user_id == user.get("id"))\
                                .first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="To Do not found!")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
