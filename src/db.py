from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from .config import DbConfig
from .logging_config import get_logger


logger = get_logger(__name__)


def create_db_engine(db_config: DbConfig) -> Engine:
    url = (
        "mysql+pymysql://"
        f"{db_config.user}:{db_config.password}"
        f"@{db_config.host}:{db_config.port}/{db_config.name}"
    )

    logger.info("Creating database engine for host=%s db=%s", db_config.host, db_config.name)
    engine = create_engine(url, echo=db_config.echo, future=True)
    return engine


def create_session_factory(engine: Engine):
    """Return a configured SQLAlchemy session factory."""
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)