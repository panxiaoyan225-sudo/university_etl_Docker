from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class UniversityRanking(Base):
    __tablename__ = "university_rankings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    province = Column(String(100), nullable=True)
    alpha_two_code = Column(String(10), nullable=True)
    web_pages = Column(String(1000), nullable=True)
    domain = Column(String(255), nullable=False)
    load_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("name", "country", "domain", name="uq_university_unique"),
    )
    