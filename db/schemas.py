import uuid
import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    phone_number: str


class User(UserBase):
    id: uuid.UUID
    phone_number: str
    class Config:
        orm_mode = True



class GroupMemberBase(BaseModel):
    user_id: uuid.UUID


class GroupMemberCreate(GroupMemberBase):
    pass


class GroupMember(GroupMemberBase):
    group_id: uuid.UUID

    class Config:
        orm_mode = True



class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: uuid.UUID
    # members: list[GroupMember] = []

    class Config:
        orm_mode = True



class ExpenseUserBase(BaseModel):
    user_id: uuid.UUID
    amount_paid: int
    amount_owed: int
    net_balance: int


class ExpenseUserCreate(ExpenseUserBase):
    pass


class ExpenseUser(ExpenseUserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    date: datetime.date
    total_amount: int
    description: str


class ExpenseCreate(ExpenseBase):
    users: list[ExpenseUserCreate]
    group_id: uuid.UUID


class Expense(ExpenseBase):
    id: uuid.UUID
    users: list[ExpenseUser] = []
    group_id: uuid.UUID

    class Config:
        orm_mode = True

