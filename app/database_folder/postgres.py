from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import create_database, database_exists
from app.database_folder.db_setting import settings
from logger import logger


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    settings.DATABASE_URL_asyncpg,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    future=True,
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
    try:
        engine = create_sync_engine()
        if not database_exists(engine.url):
            create_database(engine.url)
            with engine.begin() as conn:
                Base.metadata.create_all(bind=conn)
            print(f'Created database: "{engine.url}"')
        else:
            print(f'Database "{engine.url}" already exists')
            # Проверяем, что таблицы существуют
            try:
                with engine.begin() as conn:
                    Base.metadata.create_all(bind=conn)
                print('Tables verified/created successfully')
            except Exception as e:
                print(f'Warning: Could not verify tables: {e}')
    except Exception as e:
        print(f'Error in postgres_check_and_create_database: {e}')
        raise


def drop_database_if_exists():
    try:
        admin_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
        engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
        with engine.connect() as conn:
            # Сначала отключаем все активные соединения
            conn.execute(
                text("SELECT pg_terminate_backend(pid) "
                     "FROM pg_stat_activity WHERE datname = :dbname AND pid <> pg_backend_pid()"),
                {"dbname": settings.DB_NAME})
            # Затем удаляем базу данных
            conn.execute(text(f'DROP DATABASE IF EXISTS "{settings.DB_NAME}"'))
        print(f'Database "{settings.DB_NAME}" dropped (if it existed)')
    except Exception as e:
        print(f'Warning: Could not drop database "{settings.DB_NAME}": {e}')
        # Не прерываем выполнение, просто продолжаем
