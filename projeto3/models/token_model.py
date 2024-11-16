from pydantic import BaseModel


class Token_Model(BaseModel):
    acess_token: str
    token_type: str
