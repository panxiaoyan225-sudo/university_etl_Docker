# Coordinates extract → transform → load; initializes DB and logging.
from sqlalchemy import text

from .config import get_config
from .db import create_db_engine
from .logging_config import configure_logging, get_logger
from .extract import extract_universities
from .transform import transform_universities
from .load import load_universities
from .models import Base


def main() -> None:
    config = get_config()
    logger = configure_logging(config.log_level)

    logger.info("Starting Hipo Labs University ETL pipeline.")

    engine = create_db_engine(config.db)

    # Ensure schema and table exist
    Base.metadata.create_all(engine)

    raw_records = extract_universities(config)
    transformed_df = transform_universities(raw_records)
    loaded_count = load_universities(engine, transformed_df)

    logger.info("ETL pipeline completed. Total rows loaded: %d", loaded_count)


if __name__ == "__main__":
    main()