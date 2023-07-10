from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


db_url = settings.DATABASE_URL
print("DB URL:", db_url)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
