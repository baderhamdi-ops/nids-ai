import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.alert import Base

DB_URL = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER','nids_user')}:"
    f"{os.getenv('POSTGRES_PASSWORD','nids_password')}@"
    f"{os.getenv('POSTGRES_HOST','localhost')}:"
    f"{os.getenv('POSTGRES_PORT','5432')}/"
    f"{os.getenv('POSTGRES_DB','nids_db')}"
)

engine       = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
