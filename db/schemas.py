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
    group_id: uuid.UUID


class GroupMemberCreate(GroupMemberBase):
    pass


class GroupMember(GroupMemberBase):
    id: uuid.UUID
    class Config:
        orm_mode = True



class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: uuid.UUID

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
    group_id: uuid.UUID
    users: list[uuid.UUID] = []
    payee: uuid.UUID
    amount_paid: int


class Expense(ExpenseBase):
    id: uuid.UUID
    users: list[ExpenseUser] = []
    group_id: uuid.UUID

    class Config:
        orm_mode = True


class GroupExpense(ExpenseBase):
    id: uuid.UUID
    user: uuid.UUID
    group: uuid.UUID

    class Config:
        orm_mode = True

