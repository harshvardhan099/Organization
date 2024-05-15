import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from schema.organization_schema import OrganizationCreate, OrganizationRead
from service.organization_service import create_company_service, get_all_companies_service
from database import get_db, engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.post("/getOrganizations/")
def create_company(company: OrganizationCreate, db: Session = Depends(get_db)):
  return create_company_service(db, company.name)


@app.get("/getOrganization/")
def read_companies(db: Session = Depends(get_db)):
  return get_all_companies_service(db)


if __name__ == '__main__':
  uvicorn.run(app)
