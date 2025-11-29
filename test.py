from library.db import Base, engine
from library.models import Author, Book, Student, Borrow
from library import services

# Kutubxona bazasini yaratish (jadval va bog'lanishlar)
Base.metadata.create_all(bind=engine)

# Muallif yaratamiz va ID, ismni chiqaramiz
muallif = services.create_author("J.K. Rowling", "Britaniyalik muallif")
print(muallif.id, muallif.name, "- muallif ID va ismi")

# Talaba yaratamiz va ID, ismni chiqaramiz
# Email takrorlansa xatolik chiqadi
student = services.create_student("Tolibova Farangiz", "tolibova@example.com")
if student:
    print(student.id, student.full_name, "- talaba ID va F.I.Sh")
    # Kitob yaratamiz va ID, nomini chiqaramiz
    kitob = services.create_book("Garri Potter 1", muallif.id, 1997)
    print(kitob.id, kitob.title, "- kitob ID va nomi")
    # Talabaga kitob beramiz
    olindi = services.borrow_book(student.id, kitob.id)
    print(olindi.id if olindi else "Kitob olishda xatolik", "- borrow ID yoki xabar")
    # Kitobni qaytarish
    if olindi:
        qaytdi = services.return_book(olindi.id)
        print("Qaytarildi:", qaytdi, "- qaytarilganlik holati")
    # Statistika: talaba nechta kitob olgan
    jami_olingan = services.get_student_borrow_count(student.id)
    print("Jami olingan kitoblar:", jami_olingan)
else:
    print("Talaba yaratishda xatolik: email takrorlangan")
    print("Talabaga kitob berish/statistika o'tkazilmadi")
