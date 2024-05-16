from datetime import timedelta
import jwt
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from Organization import database
from Organization.schema import organization_schema
from Organization.schema.organization_schema import OrganizationCreate, OrganizationRead
from Organization.security import organization_security
from Organization.service import organization_service
from Organization.models import organization_model
from Organization.service.organization_service import create_company_service, get_all_companies_service, \
  authenticate_user, get_user
from Organization.database import get_db, engine, Base
from main import JWTError

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_current_user(token: str = Depends(organization_security.oauth2_scheme), db: Session = Depends(database.get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, organization_security.SECRET_KEY, algorithms=[organization_security.ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = organization_schema.TokenData(username=username)
  except JWTError:
    raise credentials_exception
  user = get_user(username, db)
  if user is None:
    raise credentials_exception
  return user


@app.post("/getOrganizations/")
def create_company(company: OrganizationCreate, db: Session = Depends(get_db),
                   current_user: organization_model.User = Depends(get_current_user)):
  return create_company_service(db, company.name)


@app.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=organization_security.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = organization_security.create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}


@app.get('/companies/', response_model=List[organization_schema.OrganizationRead])
def get_companies(db: Session = Depends(database.get_db),
                  current_user: organization_model.User = Depends(get_current_user)):
  return organization_service.get_organizations(db)


if __name__ == '__main__':
  uvicorn.run(app)
