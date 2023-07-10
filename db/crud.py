import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from db import schemas
from db.db_models import User, Group, GroupMember, Expense, ExpenseUser

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
    db_group = Group(name=group.name, id=uuid.uuid4())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def add_member_to_group(
    group_id: str,
    user_id: str,
    db: Session
):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_member = GroupMember(
        id=uuid.uuid4(),
        user_id=db_user.id,
        group_id=db_group.id
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_members_of_group(
    group_id: str,
    db: Session
):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db_members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    if not db_members:
        raise HTTPException(status_code=404, detail="No users assigned")
    user_id_list =[]
    for member in db_members:
        user_id_list.append(member.user_id)

    db_users = db.query(User).filter(User.id.in_(user_id_list)).all()

    return db_users

def get_groups(db: Session, limit: int):
    db_groups = db.query(Group).limit(limit).all()
    return db_groups


def get_previous_expenses(db: Session, user_id: str, expense_id: str):
    db_expenses = db.query(ExpenseUser).filter(user_id=user_id, expense_id=expense_id).all()
    total_paid = 0
    total_owed = 0
    for expense in db_expenses:
        total_paid += expense.amount_paid
        total_owed += expense.amount_owed

    expense_details = {
        "total_paid": total_paid,
        "total_owed": total_owed
    }
    return expense_details


def create_group_expense(expense: schemas.ExpenseCreate, db: Session ):
    db_payee_user = db.query(User).filter(User.id == expense.payee).first()
    if not db_payee_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_group = db.query(Group).filter(Group.id == expense.group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    db_expense = Expense(
        id=uuid.uuid4(),
        date=expense.date,
        total_amount=expense.total_amount,
        description=expense.description,
        user=db_payee_user.id,
        group=db_group.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    
    user_id_list = expense.users if expense.users else get_members_of_group(group_id=expense.group_id, db=db)
    
    if expense.payee in user_id_list:
        user_id_list.remove(expense.payee)    


    if len(user_id_list) <= 0:
        raise HTTPException(status_code=404, detail="Can't create expense for empty group")

    # Payee paid the total amount.
    db_payee_user = ExpenseUser(
        id = uuid.uuid4(),
        user_id=expense.payee,
        amount_paid=expense.amount_paid,
        amount_owed=expense.total_amount - expense.amount_paid,
        owed_to=None,
        expense=db_expense.id
    )
    
    db.add(db_payee_user)


    
    split_amount = expense.total_amount/len(user_id_list)


    for user in user_id_list:
        db_expense_user = ExpenseUser(
            id = uuid.uuid4(),
            user_id=user.id,
            amount_paid=0,
            amount_owed=split_amount,
            owed_to=None,
            expense=db_expense.id
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


def filter_expenses_by_group(
    group_id: str,
    db: Session 
):
    db_expenses = db.query(Expense).filter(Expense.group == group_id).all()
    return db_expenses


# Get expenses by user_id along with owed and paid amounts
def get_expenses_by_user(
    user_id: str,
    db: Session 
):
    db_expenses = db.query(ExpenseUser).filter(ExpenseUser.user_id == user_id).all()
    return db_expenses