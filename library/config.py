# Muhit o'zgaruvchilarini va SQLAlchemy kutubxonasini import qilamiz
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env fayldan o'zgaruvchilarni yuklaymiz
load_dotenv()

# Agar DATABASE_URL bo'lmasa, alohida o'zgaruvchilar orqali yig'amiz
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASS', '')
    dbname = os.getenv('DB_NAME', 'exam_db')
    DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

# Engine va session yaratamiz
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# Baza jadval va bog'lanishlarni yaratish funksiyasi
def init_db():
    Base.metadata.create_all(bind=engine)