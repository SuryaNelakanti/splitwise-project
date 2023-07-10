import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from db import schemas
from db.db_models import User, Group, group_members, Expense, ExpenseUser

def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(email=user.email, phone_number=user.phone_number, name=user.name, id=uuid.uuid4())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_group(db: Session, group_id: str):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    users = db.query(User).join(Group.members).filter(Group.id == group_id).all()
    return users

def get_users(db: Session, limit: int = 100):
    return db.query(User).limit(limit).all()

def create_group(group: schemas.GroupCreate, db: Session):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def add_member_to_group(
    group_id: str,
    member: schemas.GroupMemberCreate,
    db: Session
):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db_member = group_members(
        user_id=member.user_id,
        group_id=group_id
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_groups(db: Session):
    db_groups = db.query(Group).all()
    return db_groups




def create_expense(expense: schemas.ExpenseCreate, db: Session ):
    db_expense = Expense(
        date=expense.date,
        total_amount=expense.total_amount,
        description=expense.description,
        group_id=expense.group_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    for user in expense.users:
        db_expense_user = ExpenseUser(
            user_id=user.user_id,
            amount_paid=user.amount_paid,
            amount_owed=user.amount_owed,
            net_balance=user.net_balance,
            expense=db_expense
        )
        db.add(db_expense_user)
    
    db.commit()
    db.refresh(db_expense)
    
    return db_expense


# Get expenses by expense_description
def get_expenses_by_description(
    expense_description: str,
    db: Session 
):
    db_expenses = db.query(Expense).filter(Expense.description.ilike(f"%{expense_description}%")).all()
    return db_expenses


# Filter expenses by date
def filter_expenses_by_date(
    start_date: date,
    end_date: date,
    db: Session 
):
    db_expenses = db.query(Expense).filter(Expense.date.between(start_date, end_date)).all()
    return db_expenses


# Filter expenses by user
def filter_expenses_by_user(
    user_id: str,
    db: Session 
):
    db_expenses = db.query(Expense).join(Expense.users).filter(ExpenseUser.user_id == user_id).all()
    return db_expenses
