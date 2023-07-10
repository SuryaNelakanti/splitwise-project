
import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    phone_number: str


class User(UserBase):
    id: str
    class Config:
        orm_mode = True

class GroupMemberBase(BaseModel):
    user_id: str


class GroupMemberCreate(GroupMemberBase):
    pass


class GroupMember(GroupMemberBase):
    group_id: str

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: str
    members: list[GroupMember] = []

    class Config:
        orm_mode = True


class ExpenseUserBase(BaseModel):
    user_id: str
    amount_paid: int
    amount_owed: int
    net_balance: int


class ExpenseUserCreate(ExpenseUserBase):
    pass


class ExpenseUser(ExpenseUserBase):
    id: str

    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    date: datetime.date
    total_amount: int
    description: str


class ExpenseCreate(ExpenseBase):
    users: list[ExpenseUserCreate]
    group_id: str


class Expense(ExpenseBase):
    id: str
    users: list[ExpenseUser] = []
    group_id: str

    class Config:
        orm_mode = True
