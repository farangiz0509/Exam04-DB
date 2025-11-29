from library.db import Base, engine
from library.models import Author, Book, Student, Borrow
from library import services

# DB ni yaratish
Base.metadata.create_all(bind=engine)

# AUTHOR
a1 = services.create_author("J.K. Rowling", "British author")
print(a1.id, a1.name)

# STUDENT
s1 = services.create_student("Trefan Farangiz", "trefan@example.com")
print(s1.id, s1.full_name)

# BOOK
b1 = services.create_book("Harry Potter 1", a1.id, 1997)
print(b1.id, b1.title)

# BORROW
borrow1 = services.borrow_book(s1.id, b1.id)
print(borrow1.id if borrow1 else "Borrow failed")

# RETURN
returned = services.return_book(borrow1.id)
print("Returned:", returned)

# STATISTICS
count = services.get_student_borrow_count(s1.id)
print("Total borrows:", count)
