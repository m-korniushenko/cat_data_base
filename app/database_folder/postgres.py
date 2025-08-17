from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import create_database, database_exists
from app.database_folder.db_setting import settings
from logger import logger


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)

async_session = async_sessionmaker(async_engine)


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


def create_sync_engine():
    return create_engine(settings.DATABASE_URL_syncpg)


def postgres_check_and_create_database(import_model):
    print(f"Download: {import_model.__name__}")
    engine = create_sync_engine()
    if not database_exists(engine.url):
        create_database(engine.url)
        with engine.begin() as conn:
            Base.metadata.create_all(bind=conn)
        print(f'Created database: "{engine.url}"')
    else:
        print(f'Database "{engine.url}" already exists')


def drop_database_if_exists():
    admin_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
    engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(
            text("SELECT pg_terminate_backend(pid) "
                 "FROM pg_stat_activity WHERE datname = :dbname"),
            {"dbname": settings.DB_NAME})
        conn.execute(text(f'DROP DATABASE IF EXISTS "{settings.DB_NAME}"'))

    print(f'Database "{settings.DB_NAME}" dropped (if it existed)')
