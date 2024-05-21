from typing import List, Type, Union, Optional, Any
from sqlalchemy.orm import Session
from models.organization_model import Organization, OrganizationBase, Users
from repository.organization_repository import OrganizationRepository
from security.organization_security import OrganizationSecurity


class OrganizationService:
  @staticmethod
  def create_company_service(db: Session, company_name: str) -> OrganizationBase:
    company = Organization(name=company_name)
    return OrganizationRepository.create_organization(db, company)
  
  @staticmethod
  def get_all_companies_service(db: Session) -> List[Any]:
    return OrganizationRepository.get_organizations(db)
  
  @staticmethod
  def authenticate_user(username: str, password: str, db: Session) -> Union[bool, Type[Users]]:
    user = OrganizationRepository.get_user_by_username(db, username)
    if not user:
      return False
    if not OrganizationSecurity.verify_password(password, user.hashed_password):  # type: ignore
      return False
    return user
  
  @staticmethod
  def get_user(username: str, db: Session) -> Optional[Type[Users]]:
    user = OrganizationRepository.get_user_by_username(db, username)
    if user:
      return user
    return None
