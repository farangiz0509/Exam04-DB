from .db import SessionLocal
from .models import Author, Book, Student, Borrow
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# ==================== AUTHOR CRUD ====================
def create_author(name: str, bio: str = None) -> Author:
    with SessionLocal() as session:
        author = Author(name=name, bio=bio)
        session.add(author)
        session.commit()
        session.refresh(author)
        return author

def get_author_by_id(author_id: int) -> Author | None:
    with SessionLocal() as session:
        return session.get(Author, author_id)

def get_all_authors() -> list[Author]:
    with SessionLocal() as session:
        return session.query(Author).all()

def update_author(author_id: int, name: str = None, bio: str = None) -> Author | None:
    with SessionLocal() as session:
        author = session.get(Author, author_id)
        if not author:
            return None
        if name:
            author.name = name
        if bio is not None:
            author.bio = bio
        session.commit()
        session.refresh(author)
        return author

def delete_author(author_id: int) -> bool:
    with SessionLocal() as session:
        author = session.get(Author, author_id)
        if not author or author.books:
            return False
        session.delete(author)
        return True

# ==================== BOOK CRUD ====================
def create_book(title: str, author_id: int, published_year: int, isbn: str = None) -> Book:
    with SessionLocal() as session:
        book = Book(title=title, author_id=author_id, published_year=published_year, isbn=isbn)
        session.add(book)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError("ISBN must be unique")
        session.refresh(book)
        return book

def get_book_by_id(book_id: int) -> Book | None:
    with SessionLocal() as session:
        return session.get(Book, book_id)

def get_all_books() -> list[Book]:
    with SessionLocal() as session:
        return session.query(Book).all()

def search_books_by_title(title: str) -> list[Book]:
    with SessionLocal() as session:
        return session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

def delete_book(book_id: int) -> bool:
    with SessionLocal() as session:
        book = session.get(Book, book_id)
        if not book:
            return False
        session.delete(book)
        return True

# ==================== STUDENT CRUD ====================
def create_student(full_name: str, email: str, grade: str = None) -> Student:
    with SessionLocal() as session:
        student = Student(full_name=full_name, email=email, grade=grade)
        session.add(student)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError("Email must be unique")
        session.refresh(student)
        return student

def get_student_by_id(student_id: int) -> Student | None:
    with SessionLocal() as session:
        return session.get(Student, student_id)

def get_all_students() -> list[Student]:
    with SessionLocal() as session:
        return session.query(Student).all()

def update_student_grade(student_id: int, grade: str) -> Student | None:
    with SessionLocal() as session:
        student = session.get(Student, student_id)
        if not student:
            return None
        student.grade = grade
        session.commit()
        session.refresh(student)
        return student

# ==================== BORROW/RETURN ====================
def borrow_book(student_id: int, book_id: int) -> Borrow | None:
    with SessionLocal() as session:
        student = session.get(Student, student_id)
        book = session.get(Book, book_id)
        if not student or not book or not book.is_available:
            return None
        active_borrows = session.query(Borrow).filter(
            Borrow.student_id==student_id,
            Borrow.returned_at==None
        ).count()
        if active_borrows >= 3:
            return None
        borrow = Borrow(student_id=student_id, book_id=book_id,
                        borrowed_at=datetime.utcnow(),
                        due_date=datetime.utcnow() + timedelta(days=14))
        book.is_available = False
        session.add(borrow)
        session.commit()
        session.refresh(borrow)
        return borrow

def return_book(borrow_id: int) -> bool:
    with SessionLocal() as session:
        borrow = session.get(Borrow, borrow_id)
        if not borrow or borrow.returned_at is not None:
            return False
        borrow.returned_at = datetime.utcnow()
        borrow.book.is_available = True
        session.commit()
        return True

# ==================== QUERY FUNCTIONS ====================
def get_student_borrow_count(student_id: int) -> int:
    with SessionLocal() as session:
        return session.query(Borrow).filter(Borrow.student_id==student_id).count()

def get_currently_borrowed_books() -> list[tuple[Book, Student, datetime]]:
    with SessionLocal() as session:
        results = session.query(Borrow).filter(Borrow.returned_at==None).all()
        return [(b.book, b.student, b.borrowed_at) for b in results]

def get_books_by_author(author_id: int) -> list[Book]:
    with SessionLocal() as session:
        return session.query(Book).filter(Book.author_id==author_id).all()

def get_overdue_borrows() -> list[tuple[Borrow, Student, Book, int]]:
    with SessionLocal() as session:
        overdue = session.query(Borrow).filter(
            Borrow.returned_at==None,
            Borrow.due_date < datetime.utcnow()
        ).all()
        result = []
        for b in overdue:
            days_late = (datetime.utcnow() - b.due_date).days
            result.append((b, b.student, b.book, days_late))
        return result
