from datetime import timedelta
import jwt
from jwt import PyJWTError
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Type, Dict, Union, Any
from models.organization_model import Users, OrganizationBase
from security.organization_security import OrganizationSecurity
from models import organization_model
from service.organization_service import OrganizationService, AuthenticateService
from database import Database

app = FastAPI()
Database.Base.metadata.create_all(bind=Database.engine)


class User:
  
  @staticmethod
  def get_current_user(
    token: str = Depends(OrganizationSecurity.oauth2_scheme),
    db: Session = Depends(Database.get_db)) -> Type[Users]:
    
    credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )
    try:
      payload = jwt.decode(token, OrganizationSecurity.SECRET_KEY, algorithms=[OrganizationSecurity.ALGORITHM])
      username: Union[Any, None] = payload.get("sub")
      if username is None:
        raise credentials_exception
      token_data = organization_model.TokenData(username=username)
    except PyJWTError:
      raise credentials_exception
    user = AuthenticateService.get_user(token_data.username, db)
    if user is None:
      raise credentials_exception
    return user  # type: ignore


class OrganizationRoute:
  
  @staticmethod
  @app.post("/getOrganizations/")
  def create_company(company: organization_model.OrganizationCreate,
                     db: Session = Depends(Database.get_db),
                     current_user: organization_model.User = Depends(User.get_current_user)) -> OrganizationBase:
    return OrganizationService.create_company_service(db, company.name)
  
  @staticmethod
  @app.post('/token')
  def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
                     db: Session = Depends(Database.get_db)) -> Dict[str, Union[list, str]]:  # type: ignore
    user = AuthenticateService.authenticate_user(form_data.username, form_data.password, db)
    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
      )
    access_token_expires = timedelta(minutes=OrganizationSecurity.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = OrganizationSecurity.create_access_token(data={"sub": user.username},
                                                            expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
  
  @staticmethod
  @app.get('/companies/', response_model=List[organization_model.OrganizationRead])
  def get_companies(db: Session = Depends(Database.get_db),
                    current_user: organization_model.User = Depends(User.get_current_user)) -> list:  # type: ignore
    return OrganizationService.get_all_companies_service(db)  # type: ignore


if __name__ == '__main__':
  uvicorn.run(app)
