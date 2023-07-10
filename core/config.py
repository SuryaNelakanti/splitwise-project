import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME = "Splitwise"
    POSTGRES_USER  = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER  = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT  = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB  = os.getenv("POSTGRES_DB","local_db")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()