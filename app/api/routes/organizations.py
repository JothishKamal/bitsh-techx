from fastapi import APIRouter, HTTPException
from typing import List
from app.api.models.organizations import OrganizationCreate, Organization
from app.services import organization_service

router = APIRouter()

@router.post("/organizations", response_model=Organization)
async def create_organization(org_data: OrganizationCreate):
    org = await organization_service.create_organization(org_data.name)
    return org

@router.get("/organizations/{org_id}", response_model=Organization)
async def get_organization(org_id: int):
    org = await organization_service.get_organization(org_id)
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return org

@router.get("/organizations", response_model=List[Organization])
async def get_organizations():
    orgs = await organization_service.get_organizations()
    return orgs