from pydantic import BaseModel
from typing import List, Optional

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    
    class Config:
        from_attributes = True