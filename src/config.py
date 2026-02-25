import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class ApiConfig:
    url: str
    country: str


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    name: str
    echo: bool


@dataclass
class AppConfig:
    api: ApiConfig
    db: DbConfig
    log_level: str
    project_root: str


def get_config() -> AppConfig:
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    api_url = os.getenv("API_URL", "http://universities.hipolabs.com/search")
    api_country = os.getenv("API_COUNTRY", "Canada")

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "university_db")
    sqlalchemy_echo = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    return AppConfig(
        api=ApiConfig(url=api_url, country=api_country),
        db=DbConfig(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            name=db_name,
            echo=sqlalchemy_echo,
        ),
        log_level=log_level,
        project_root=project_root,
    )