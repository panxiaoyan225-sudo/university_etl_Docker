# Coordinates extract → transform → load; initializes DB and logging.
from sqlalchemy import text

from .config import get_config
from .db import create_db_engine
from .logging_config import configure_logging, get_logger
from .extract import extract_universities
from .transform import transform_universities
from .load import load_universities
from .models import Base



# The use of 'None' in the return annotation (-> None) indicates that the function does not return any value.
def main() -> None:
    """
    The main function acts as the entry point for the ETL (Extract-Transform-Load) pipeline
    for the Hipo Labs University project. It orchestrates the following steps:

    1. Loads configuration values, including database connection details and log level.
    2. Configures logging so that pipeline progress and issues are recorded.
    3. Establishes a database connection using SQLAlchemy, and creates the necessary tables if they do not exist yet.
    4. Extracts raw university data from an external source/API.
    5. Transforms this raw data into a structured dataframe suitable for database loading.
    6. Loads the transformed data into the target database.
    7. Logs how many records were loaded and when the pipeline completes.
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