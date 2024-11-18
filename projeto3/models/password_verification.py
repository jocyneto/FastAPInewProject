from pydantic import BaseModel


class PasswordVerification(BaseModel):
    password: str
    new_password: str 
