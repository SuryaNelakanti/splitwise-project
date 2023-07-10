from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_model import BaseMeta
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(BaseMeta):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    members = Column(UUID(as_uuid=True), ForeignKey('groupmember.id'), index=True, nullable=True)


class GroupMember(BaseMeta):
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    group_id = Column(UUID(as_uuid=True), ForeignKey('group.id'))

