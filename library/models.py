# SQLAlchemy kutubxonalarini import qilamiz
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timedelta

# Baza uchun asosiy klass
Base = declarative_base()

# Muallif modeli
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    name = Column(String(100), nullable=False)  # Muallif ismi
    bio = Column(Text, nullable=True)  # Biografiya
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Yaratilgan vaqt
    books = relationship('Book', back_populates='author', cascade='all, delete-orphan')  # Muallifning kitoblari

# Kitob modeli
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    title = Column(String(200), nullable=False)  # Sarlavha
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)  # Muallif ID
    published_year = Column(Integer)  # Chop etilgan yil
    isbn = Column(String(13), unique=True, nullable=True)  # ISBN
    is_available = Column(Boolean, default=True)  # Bandlik holati
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Yaratilgan vaqt
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # Yangilangan vaqt
    author = relationship('Author', back_populates='books')  # Muallif bilan bog'lanish
    borrows = relationship('Borrow', back_populates='book', cascade='all, delete-orphan')  # Borrowlar

# Talaba modeli
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    full_name = Column(String(150), nullable=False)  # F.I.Sh
    email = Column(String(100), unique=True, nullable=False)  # Email
    grade = Column(String(20), nullable=True)  # Sinf
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Ro'yxatdan o'tgan vaqt
    borrows = relationship('Borrow', back_populates='student', cascade='all, delete-orphan')  # Borrowlar

# Borrow modeli
class Borrow(Base):
    __tablename__ = 'borrows'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)  # Talaba ID
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)  # Kitob ID
    borrowed_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Olingan vaqt
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14), nullable=False)  # Qaytarish muddati
    returned_at = Column(DateTime, nullable=True)  # Qaytarilgan vaqt
    student = relationship('Student', back_populates='borrows')  # Talaba bilan bog'lanish
    book = relationship('Book', back_populates='borrows')  # Kitob bilan bog'lanish
