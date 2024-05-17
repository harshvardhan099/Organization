from typing import Union

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Database


class Organization(Database.Base):
  __tablename__ = 'companies'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)


class Users(Database.Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)


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
