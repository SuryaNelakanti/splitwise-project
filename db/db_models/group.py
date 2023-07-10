from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_model import BaseMeta
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(BaseMeta):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    members = relationship("user", secondary="group_members")


group_members = Table(
    'group_members', Base.metadata,
    Column('group_id', String, ForeignKey('group.id')),
    Column('user_id', String, ForeignKey('user.id'))
)
