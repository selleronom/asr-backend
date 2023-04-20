from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

sqlalchemy_database_uri = "postgresql+asyncpg://admin:password@db/db"

engine = create_async_engine(sqlalchemy_database_uri)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
