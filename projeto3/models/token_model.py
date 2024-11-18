from pydantic import BaseModel


class Token_Model(BaseModel):
    access_token: str
    token_type: str
