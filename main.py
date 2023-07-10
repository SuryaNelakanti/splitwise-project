from fastapi import FastAPI, Depends

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

@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    db_user = crud.create_user(db=db, user=user)
    return db_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db,  limit=limit)
    return users


@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.create_group(db=db, group=group)
    return db_group

# Add a member to a group
@app.post("/groups/{group_id}/members/", response_model=schemas.Group)
def add_member_to_group(
    group_id: str,
    member: schemas.GroupMemberCreate,
    db: Session = Depends(get_db)
):
    db_group = crud.add_member_to_group(group_id=group_id, member=member, db=db)
    return db_group

@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = crud.create_expense(db=db, expense=expense)
    return db_expense


# Get expenses by expense_description
@app.get("/expenses/{expense_description}", response_model=list[schemas.Expense])
def get_expenses_by_description(
    expense_description: str,
    db: Session = Depends(get_db)
):
    db_expenses = crud.get_expenses_by_description(db, expense_description=expense_description)
    return db_expenses


# Filter expenses by date
@app.get("/expenses/filter/date/", response_model=list[schemas.Expense])
def filter_expenses_by_date(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    db_expenses = crud.filter_expenses_by_date(db, start_date=start_date, end_date=end_date)
    return db_expenses


# Filter expenses by user
@app.get("/expenses/filter/user/{user_id}", response_model=list[schemas.Expense])
def filter_expenses_by_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    db_expenses = crud.filter_expenses_by_user(db, user_id=user_id)
    return db_expenses