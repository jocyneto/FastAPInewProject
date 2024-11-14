from pydantic import BaseModel


class User_Model(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role:str
