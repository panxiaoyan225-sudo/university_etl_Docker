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
    """
    Main entry point for the Hipo Labs University ETL pipeline.

    This function orchestrates the Extract-Transform-Load (ETL) process:
    1. Loads configuration settings (including database and logging details).
    2. Configures logging for the pipeline.
    3. Initializes the database connection and ensures required tables exist.
    4. Extracts raw university data from the external source/API.
    5. Transforms the extracted data into the desired structure and format.
    6. Loads the transformed data into the destination database.
    7. Logs the completion and number of rows loaded.
    """
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