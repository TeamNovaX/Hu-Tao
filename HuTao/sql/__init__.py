from logging import getLogger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from HuTao import SQL_URL
LOGGER = getLogger(__name__)

if SQL_URL and SQL_URL.startswith("postgres://"):
    DB_URI = SQL_URL.replace("postgres://", "postgresql://", 1)


def start() -> scoped_session:
    engine = create_engine(SQL_URL, client_encoding="utf8")
    LOGGER.info("[PostgreSQL] Connecting to database......")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
try:
    SESSION = start()
except Exception as e:
    LOGGER.info(f"[PostgreSQL] Failed to connect due to {e}")
    exit()

LOGGER.info("[PostgreSQL] Connection successful, session started.")