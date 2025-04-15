from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DB_URL, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
# expire_on_commit=False: Этот параметр указывает, что после выполнения операции commit объекты,
# связанные с сессией, не будут "истекать" (т.е. их данные сохранятся в памяти)

async def get_db():
    async with async_session() as session:
        yield session
