from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String
from db.base_model import BaseMeta


class User(BaseMeta):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone_number = Column(String(14), nullable=False, unique=True, index=True)
    # Since POC, no need for password.
