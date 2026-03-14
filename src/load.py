from typing import List, Dict, Any

import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.dialects.mysql import insert as mysql_insert

from .logging_config import get_logger
from .models import UniversityRanking


logger = get_logger(__name__)


def load_universities(engine: Engine, df: pd.DataFrame, chunk_size: int = 500) -> int:
    if df.empty:
        logger.warning("No data to load into database.")
        return 0

    total_rows = len(df)
    logger.info("Starting load of %d rows into university_rankings.", total_rows)

    rows_loaded = 0

    with engine.begin() as conn:
        for start in range(0, total_rows, chunk_size):
            end = start + chunk_size
            chunk = df.iloc[start:end]
            records: List[Dict[str, Any]] = chunk.to_dict(orient="records")

            stmt = mysql_insert(UniversityRanking).values(records)

            update_cols = {
                "country": stmt.inserted.country,
                "province": stmt.inserted.province,
                "alpha_two_code": stmt.inserted.alpha_two_code,
                "web_pages": stmt.inserted.web_pages,
                "load_timestamp": stmt.inserted.load_timestamp,
            }

            upsert_stmt = stmt.on_duplicate_key_update(**update_cols)

            conn.execute(upsert_stmt)
            rows_loaded += len(records)

            logger.info(
                "Loaded chunk %d-%d (%d rows).",
                start,
                min(end, total_rows),
                len(records),
            )

    logger.info("Completed loading %d rows into university_rankings.", rows_loaded)
    return rows_loaded