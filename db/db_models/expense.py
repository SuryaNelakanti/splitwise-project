from sqlalchemy import  Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from db.base_model import BaseMeta


class Expense(BaseMeta):
    id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(Date, nullable=False)
    total_amount = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)

    user = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
    group = Column(UUID(as_uuid=True), ForeignKey("group.id"), index=True)
