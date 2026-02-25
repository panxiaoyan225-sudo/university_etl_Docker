import json
import os
from datetime import datetime
from typing import Any, Dict, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import ApiConfig, AppConfig
from .logging_config import get_logger


logger = get_logger(__name__)


def _create_session_with_retries() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def extract_universities(config: AppConfig) -> List[Dict[str, Any]]:
    session = _create_session_with_retries()
    params = {"country": config.api.country}

    logger.info("Requesting universities from %s with params=%s", config.api.url, params)

    try:
        response = session.get(config.api.url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error("API request failed: %s", exc)
        raise

    try:
        data = response.json()
    except ValueError as exc:
        logger.error("Failed to parse API response JSON: %s", exc)
        raise

    if not isinstance(data, list):
        logger.error("Unexpected API response format: expected list, got %s", type(data))
        raise ValueError("Unexpected API response format")

    logger.info("Successfully fetched %d records from API", len(data))

    _persist_bronze_snapshot(config, data)

    return data


def _persist_bronze_snapshot(config: AppConfig, data: List[Dict[str, Any]]) -> None:
    bronze_dir = os.path.join(config.project_root, "data", "bronze")
    os.makedirs(bronze_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    file_path = os.path.join(
        bronze_dir, f"universities_canada_raw_{timestamp}.json"
    )

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Bronze snapshot written to %s", file_path)
    except OSError as exc:
        logger.error("Failed to write bronze snapshot: %s", exc)