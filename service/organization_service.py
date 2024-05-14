from sqlalchemy.orm import Session
from repository.organization_repository import get_organizations, create_organization
from models.organization_model import Organization

def create_company_service(db: Session, company_name: str):
    company = Organization(name=company_name)
    return create_organization(db, company)

def get_all_companies_service(db: Session):
    return get_organizations(db)
