import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Compose DATABASE_URL from individual env vars if not set
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASS', '')
    dbname = os.getenv('DB_NAME', 'exam_db')
    DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)