# Baza bilan ishlash uchun kerakli kutubxonalarni import qilamiz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# .env fayldan ma'lumotlarni yuklaymiz
load_dotenv()

# DATABASE_URL ni olamiz
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine va session yaratamiz
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Baza uchun asosiy klass
Base = declarative_base()

# Barcha jadval va bog'lanishlarni yaratish funksiyasi
def init_db():
    Base.metadata.create_all(bind=engine)
