from sqlalchemy.orm import Session
from Organization.models.organization_model import Organization
from Organization.models import organization_model
from Organization.schema.organization_schema import OrganizationBase


def get_organizations(db: Session):
  return db.query(Organization).all()


def create_organization(db: Session, company: OrganizationBase):
  db.add(company)
  db.commit()
  db.refresh(company)
  return company


def get_user_by_username(db: Session, username: str):
  return db.query(organization_model.User).filter(organization_model.User.username == username).first()
