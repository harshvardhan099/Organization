from sqlalchemy.orm import Session
from Organization.repository.organization_repository import get_organizations, create_organization
from Organization.models.organization_model import Organization
from Organization.repository import organization_repository
from Organization.security import organization_security


def create_company_service(db: Session, company_name: str):
  company = Organization(name=company_name)
  return create_organization(db, company)


def get_all_companies_service(db: Session):
  return get_organizations(db)


def authenticate_user(username: str, password: str, db: Session):
  user = organization_repository.get_user_by_username(db, username)
  if not user:
    return False
  if not organization_security.verify_password(password, user.hashed_password):
    return False
  return user


def get_user(username: str, db: Session):
  user = organization_repository.get_user_by_username(db, username)
  if user:
    return user
  return None
