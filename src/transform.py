from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from .logging_config import get_logger


logger = get_logger(__name__)


def _normalize_list_field(value: Any) -> str:
    if isinstance(value, list):
        return ",".join(str(v).strip() for v in value if v is not None)
    if value is None:
        return ""
    return str(value)


def transform_universities(records: List[Dict[str, Any]]) -> pd.DataFrame:
    if not records:
        logger.warning("No records received for transformation.")
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Normalize list fields
    df["web_pages"] = df.get("web_pages", []).apply(_normalize_list_field)
    df["domain"] = df.get("domains", []).apply(_normalize_list_field)

    # Standardize province mapping from 'state-province'
    if "state-province" in df.columns:
        df["province"] = df["state-province"].fillna("")
    else:
        df["province"] = ""

    # Add load timestamp
    load_ts = datetime.utcnow()
    df["load_timestamp"] = load_ts

    # Select and rename columns
    df["name"] = df["name"].astype(str)
    df["country"] = df["country"].astype(str)
    if "alpha_two_code" not in df.columns:
        df["alpha_two_code"] = ""

    result = df[
        [
            "name",
            "country",
            "province",
            "alpha_two_code",
            "web_pages",
            "domain",
            "load_timestamp",
        ]
    ]

    _validate_transformed_data(result)

    logger.info(
        "Transformation completed. Output rows: %d, columns: %s",
        len(result),
        list(result.columns),
    )

    return result


def _validate_transformed_data(df: pd.DataFrame) -> None:
    invalid = df[df["name"].isna() | (df["name"].astype(str).str.strip() == "")]
    invalid |= df["domain"].isna() | (df["domain"].astype(str).str.strip() == "")

    # After building boolean series, filter rows
    invalid_rows = df[
        (df["name"].isna() | (df["name"].astype(str).str.strip() == ""))
        | (df["domain"].isna() | (df["domain"].astype(str).str.strip() == ""))
    ]

    if not invalid_rows.empty:
        logger.warning(
            "Found %d rows with invalid 'name' or 'domain'. They will be dropped.",
            len(invalid_rows),
        )
        logger.debug("Invalid rows sample:\n%s", invalid_rows.head())

        df.drop(index=invalid_rows.index, inplace=True)
        df.reset_index(drop=True, inplace=True)

    if df.empty:
        logger.error("All rows were invalid after validation. Nothing to load.")
        raise ValueError("No valid records after validation.")