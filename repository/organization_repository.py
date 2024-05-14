from sqlalchemy.orm import Session
from models.organization_model import Organization
from schema.organization_schema import OrganizationBase


def get_organizations(db: Session):
  return db.query(Organization).all()


def create_organization(db: Session, company: OrganizationBase):
  db.add(company)
  db.commit()
  db.refresh(company)
  return company
