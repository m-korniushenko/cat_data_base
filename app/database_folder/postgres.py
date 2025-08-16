from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import create_database, database_exists
from db_setting import settings
from logger import logger


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)

async_session = async_sessionmaker(async_engine)


def create_sync_engine():
    sync_session = create_engine(url=settings.DATABASE_URL_syncpg)
    engine = create_engine(sync_session.url)
    return engine


def check_db_connection():
    engine = create_sync_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            msg = "Database connection successful."
            logger.info(msg)
            print(msg)
            return True
    except Exception as ex:
        logger.error(f"Database connection failed: {ex}")
        return False


def postgres_check_and_create_database():
    engine = create_sync_engine()
    if not database_exists(engine.url):
        create_database(engine.url)
        with engine.begin() as conn:
            Base.metadata.create_all(bind=conn)
        print(f'Created database: "{engine.url}"')
    else:
        print(f'Database "{engine.url}" already exists')
