from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.api.models.forms import FormCreate, Form
from app.services import form_service

router = APIRouter()

@router.post("/forms", response_model=Form)
async def create_form(form_data: FormCreate):
    form = await form_service.create_form(
        form_data.name,
        form_data.description,
        form_data.organization_id,
        form_data.form_schema,
        [field.dict() for field in form_data.fields]
    )
    
    return form

@router.get("/forms/{form_id}", response_model=Form)
async def get_form(form_id: int):
    form = await form_service.get_form(form_id)
    
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    return form

@router.get("/forms", response_model=List[Form])
async def get_forms(org_id: Optional[int] = None):
    forms = await form_service.get_forms(org_id)
    return forms