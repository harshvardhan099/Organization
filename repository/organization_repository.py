from typing import List, Type, Optional
from sqlalchemy.orm import Session
from models.organization_model import Organization, OrganizationBase, Users
from models import organization_model


class OrganizationRepository:
  @staticmethod
  def get_organizations(db: Session) -> List[Type[Organization]]:
    return db.query(Organization).all()
  
  @staticmethod
  def create_organization(db: Session, company: OrganizationBase) -> OrganizationBase:
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
  
  @staticmethod
  def get_user_by_username(db: Session, username: str) -> Optional[Type[Users]]:
    return db.query(organization_model.Users).filter(organization_model.Users.username == username).first()
