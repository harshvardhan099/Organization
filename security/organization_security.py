from datetime import datetime, timedelta
from typing import Optional, Dict, Union
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


class OrganizationSecurity:
  SECRET_KEY = "4a46e01f8b396467af95afc8cfb2bed55621bc0da98f1fc0f6b965cfbc03ca39"
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30
  
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  
  @staticmethod
  def create_access_token(data: Dict[str, datetime], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
      expire = datetime.utcnow() + expires_delta
    else:
      expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, OrganizationSecurity.SECRET_KEY, algorithm=OrganizationSecurity.ALGORITHM)
    return encoded_jwt
  
  @staticmethod
  def verify_password(plain_password: str, hashed_password: Union[str, bytes, None]) -> bool:
    return OrganizationSecurity.pwd_context.verify(plain_password, hashed_password)
  
  @staticmethod
  def get_password_hash(password: str) -> str:
    return OrganizationSecurity.pwd_context.hash(password)
