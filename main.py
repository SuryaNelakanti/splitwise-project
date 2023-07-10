from fastapi import FastAPI

from core import Settings

from db.base_model import BaseMeta
from db.session import engine



def create_tables():         
	BaseMeta.metadata.create_all(bind=engine)

def start_app():
    app = FastAPI(title=Settings.PROJECT_NAME)
    create_tables()
    return app

app = start_app()


@app.get("/")
async def ping():
	return {"message":"I am alive"}



@app.get("/user")
async def get_user():
    
    return {"message":"Hello User"}