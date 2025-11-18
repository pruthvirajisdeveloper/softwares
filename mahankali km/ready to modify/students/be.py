from database import init_pool
from database.db_init import init_db
from database.sop import db_load_students, db_add_student, db_update_student

# ===================== STUDENT CLASS ===============================

class Student:
    def __init__(self, id, name, address, gender, bday, age, joindate):
        self.id = id
        self.name = name
        self.address = address
        self.gender = gender
        self.bday = bday
        self.age = age
        self.joindate = joindate

    def getimfo(self):
        """Return UI-friendly ordering"""
        return [
            self.id,
            self.name,
            self.gender,
            self.age,
            self.address,
            self.bday,
            self.joindate,
        ]

    def update(self):
        """Update database"""
        db_update_student(self)

    def __str__(self):
        return f"Student(id={self.id}, name='{self.name}', gender={self.gender}, age={self.age}, address='{self.address}')"


# ===================== MANAGER ===============================

Students = []

def newstudent(id, name, address, gender, bday, age, joindate):
    if not all([name, address, gender, bday, age]):
        return "Missing information"

    s = Student(id=id, name=name, address=address, gender=gender, bday=bday, age=age, joindate=joindate)
    new_id = db_add_student(s)
    s.id = new_id

    Students.append(s)
    return s


def printstudentimfo():
    for s in Students:
        id, name, gender, age, address, join = s.getimfo()[:6]
        print(
            f"name     : {name}\n"
            f"id       : {id}\n"
            f"gender   : {gender}\n"
            f"age      : {age}\n"
            f"address   : {address}\n"
            f"joindate : {join}\n"
            f"{'-'*40}\n"
        )


def filltable():
    init_pool()
    init_db()

    Students.clear()
    rows = db_load_students()

    for r in rows:
        id, name, address, gender, bday, age, join = r
        Students.append(Student(id, name, address, gender, bday, age, join))


if __name__ == "__main__":
    filltable
    printstudentimfo()
