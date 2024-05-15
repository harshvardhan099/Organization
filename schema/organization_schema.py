from pydantic import BaseModel


class OrganizationBase(BaseModel):
  name: str


class OrganizationCreate(OrganizationBase):
  pass


class OrganizationRead(OrganizationBase):
  id: int
  
  class Config:
    orm_mode = True
