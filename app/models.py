from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
)
from database.base import Base
from database.manager import Manager


class User(Base, Manager):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer(), nullable=True)
    tg_username = Column(String(150), nullable=False, unique=True)
    profile_username = Column(String(128), nullable=True, unique=True)
    profile_password = Column(String(128), nullable=True)
    is_superuser = Column(Boolean(), nullable=False, default=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    is_active = Column(Boolean(), nullable=False, default=True)
    date_joined = Column(DateTime(), nullable=False)
    phone = Column(String(20), nullable=True)

    def __str__(self):
        return f"User: TG:{self.tg_id} ({self.tg_username})"
