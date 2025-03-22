from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class FormFieldBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    required: bool = False
    options: Optional[Dict[str, Any]] = None

class FormFieldCreate(FormFieldBase):
    pass

class FormField(FormFieldBase):
    id: int
    formId: int
    
    class Config:
        from_attributes = True

class FormBase(BaseModel):
    name: str
    description: Optional[str] = None

class FormCreate(FormBase):
    organization_id: int
    form_schema: Dict[str, Any]
    fields: List[FormFieldCreate]

class Form(FormBase):
    id: int
    organizationId: int
    formSchema: Dict[str, Any]
    fields: List[FormField] = []
    
    class Config:
        from_attributes = True