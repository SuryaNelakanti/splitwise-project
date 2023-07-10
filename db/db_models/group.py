from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from db.base_model import BaseMeta


class Group(BaseMeta):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(255), nullable=False)