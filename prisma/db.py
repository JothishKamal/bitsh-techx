from prisma import Prisma

# Client singleton
prisma = Prisma()

async def init_db():
    await prisma.connect()

async def close_db():
    await prisma.disconnect()