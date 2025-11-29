from library.db import Base, engine
from library.models import Author, Book, Student, Borrow
from library import services

# Kutubxona DB ni yaratish (barcha jadval va bog'lanishlar)
Base.metadata.create_all(bind=engine)

# Muallif yaratish va ID, ismni chiqarish
# Bu yerda yangi muallif obyektini bazaga qo'shamiz
a1 = services.create_author("J.K. Rowling", "British author")
print(a1.id, a1.name)  # Muallif ID va ismi

# Talaba yaratish va ID, ismni chiqarish
# Email unikal bo'lishi kerak, takrorlansa xatolik chiqadi
s1 = services.create_student("Tolibova Farangiz", "tolibova@example.com")
if s1:
    print(s1.id, s1.full_name)  # Talaba ID va ism
    # Kitob yaratish va ID, nomini chiqarish
    b1 = services.create_book("Harry Potter 1", a1.id, 1997)
    print(b1.id, b1.title)  # Kitob ID va nomi
    # Talabaga kitob berish (borrow)
    borrow1 = services.borrow_book(s1.id, b1.id)
    print(borrow1.id if borrow1 else "Borrow failed")  # Agar borrow muvaffaqiyatli bo'lsa ID chiqadi
    # Kitobni qaytarish (return)
    if borrow1:
        returned = services.return_book(borrow1.id)
        print("Returned:", returned)  # True yoki False chiqadi
    # Statistika: talaba nechta kitob olganini chiqarish
    count = services.get_student_borrow_count(s1.id)
    print("Total borrows:", count)
else:
    print("Student creation failed: email already exists")  # Email takrorlangan bo'lsa
    print("Skipping borrow/return/statistics due to student creation failure.")
