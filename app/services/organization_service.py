from prisma.db import prisma

async def create_organization(name: str):
    return await prisma.organization.create(
        data={"name": name}
    )

async def get_organization(org_id: int):
    return await prisma.organization.find_unique(
        where={"id": org_id}
    )

async def get_organizations():
    return await prisma.organization.find_many()