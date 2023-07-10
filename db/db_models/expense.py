from sqlalchemy import  Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from db.base_model import BaseMeta


class Expense(BaseMeta):
    id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(Date, nullable=False)
    total_amount = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)

    users = relationship("ExpenseUser", secondary="expense_users")
    group = Column(UUID(as_uuid=True), ForeignKey("group.id"), index=True)


class ExpenseUser(BaseMeta):
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    amount_paid = Column(Integer, default=0)
    amount_owed = Column(Integer, default=0)
    net_balance = Column(Integer, default=0)
    user = relationship("UserProfile", backref="expense_user")