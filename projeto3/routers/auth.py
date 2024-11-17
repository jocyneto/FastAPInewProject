from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from models.users_model import User_Model
from models.token_model import Token_Model
from tables import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

# region generaly configs
router = APIRouter(prefix="/auth", tags=["auth"])

SECRETE_KEY = "7239c3788d35e461ca218721bad9186f40869f9f2a7cdf21a85229e88a1d2f27" # openssl rand -hex 32
ALGORITHM = "HS256"


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

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
#endregion

# region Util Funcs 
def autenticate_user(username: str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id:int, expires_delta:timedelta):
    encode = { "sub": username, "id":user_id } # A
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRETE_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
     try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # relacionado com linha com comentario A
        user_id: str = payload.get("id") # relacionado com linha com comentario A
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Não foi possivel validar usuário.")
        return {"username": username, "id": user_id}
     except JWTError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Não foi possivel validar usuário.")
#endregion

# region Requests Methods
@router.post("/add", status_code=status.HTTP_201_CREATED)
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

@router.post("/token", response_model=Token_Model)
async def login_for_acess_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependecy):
    # return form_data.username
    user = autenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed Authentication"
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"acess_token": token, "token_type": "bearer"}
#endregion
