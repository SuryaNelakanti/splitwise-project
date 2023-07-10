from fastapi import FastAPI, Depends, HTTPException

from core import Settings
from db import crud, schemas
from sqlalchemy.orm import Session
from datetime import date
from db.base_model import BaseMeta
from db.session import engine



def create_tables():         
	BaseMeta.metadata.create_all(bind=engine)

def start_app():
    app = FastAPI(title=Settings.PROJECT_NAME)
    create_tables()
    return app

app = start_app()

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def ping():
	return {"message":"I am alive"}

@app.post("/user/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
         raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db=db, user=user)
    return db_user

@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def get_users(limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db,  limit=limit)
    return users


@app.post("/group/", response_model=schemas.Group, tags=["Groups"])
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.create_group(db=db, group=group)
    return db_group

@app.get("/group/", response_model=list[schemas.Group], tags=["Groups"])
def get_group(limit: int =100, db: Session = Depends(get_db)):
    db_group = crud.get_groups(db=db, limit=limit)
    return db_group


# Add a member to a group
@app.post("/group_members/", tags=["Groups"])
def add_member_to_group(
    group_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    crud.add_member_to_group(group_id=group_id, user_id=user_id, db=db)
    return {"message": "Member added to group"}

@app.get("/group_members/", response_model=list[schemas.UserBase], tags=["Groups"])
def get_members_of_group(
    group_id: str,
    db: Session = Depends(get_db)
):
    db_users = crud.get_members_of_group(group_id=group_id, db=db)

    return db_users


@app.post("/group_expense/", response_model=schemas.GroupExpense, tags=["Expenses"])
def create_group_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = crud.create_group_expense(db=db, expense=expense)
    return db_expense

@app.get("/group_expense/", response_model=list[schemas.GroupExpense], tags=["Expenses"])
def filter_expenses_by_group(
    group_id: str,
    db: Session = Depends(get_db)
):
    db_expenses = crud.filter_expenses_by_group(db=db, group_id=group_id)
    return db_expenses


# Get expenses by user_id along with owed and paid amounts
@app.get("/user_expense/", response_model=list[schemas.UserExpense], tags=["Expenses"])
def get_expenses_by_user(user_id: str, db: Session = Depends(get_db)):
    db_expenses = crud.get_expenses_by_user(db=db, user_id=user_id)
    return db_expenses

# # Get expenses by expense_description
# @app.get("/expenses/{expense_description}", response_model=list[schemas.Expense])
# def get_expenses_by_description(
#     expense_description: str,
#     db: Session = Depends(get_db)
# ):
#     db_expenses = crud.get_expenses_by_description(db, expense_description=expense_description)
#     return db_expenses


# # Filter expenses by date
# @app.get("/expenses/filter/date/", response_model=list[schemas.Expense])
# def filter_expenses_by_date(
#     start_date: date,
#     end_date: date,
#     db: Session = Depends(get_db)
# ):
#     db_expenses = crud.filter_expenses_by_date(db, start_date=start_date, end_date=end_date)
#     return db_expenses

