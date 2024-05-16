from typing import Union

from pydantic import BaseModel


class OrganizationBase(BaseModel):
  name: str


class OrganizationCreate(OrganizationBase):
  pass


class OrganizationRead(OrganizationBase):
  id: int
  
class User(BaseModel):
    username: str


class UserInDB(User):
  hashed_password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: Union[str, None] = None
  
  class Config:
    orm_mode = True

