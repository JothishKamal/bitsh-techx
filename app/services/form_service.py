from prisma.db import prisma
from utility.generate_embedding import generate_form_embeddings, generate_embedding
from typing import Dict, Any, List

async def create_form(name: str, description: str, organization_id: int, form_schema: Dict[str, Any], fields: List[Dict[str, Any]]):
    # Generate form-level embedding
    form_embedding = generate_form_embeddings(name, description)
    
    # Create the form
    form = await prisma.form.create(
        data={
            "name": name,
            "description": description,
            "organization_id": organization_id,
            "form_schema": form_schema,
            "embedding": form_embedding,
        }
    )
    
    # Create form fields with embeddings
    for field in fields:
        field_embedding = generate_embedding(field.get("description", "")) if field.get("description") else []
        await prisma.formfield.create(
            data={
                "form_id": form.id,
                "name": field["name"],
                "description": field.get("description"),
                "type": field["type"],
                "required": field.get("required", False),
                "options": field.get("options", {}),
                "embedding": field_embedding,
            }
        )
    
    return form

async def get_form(form_id: int):
    return await prisma.form.find_unique(
        where={"id": form_id},
        include={"fields": True}
    )

async def get_forms(org_id=None):
    where = {"organization_id": org_id} if org_id else {}
    return await prisma.form.find_many(
        where=where,
        include={"organization": True}
    )