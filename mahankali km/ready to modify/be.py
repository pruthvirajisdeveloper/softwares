import time
from studentlist import stdlist


class Student:
    def __init__(self, name, id, adress, gender, bday, age, joindate):
        self.name = name
        self.id = id
        self.adress = adress
        self.gender = gender
        self.bday = bday
        self.age = age
        self.joindate = joindate

    def getimfo(self):
        return [
            self.id,
            self.name,
            self.gender,
            self.age,
            self.adress,
            self.joindate
        ]

    def edit(self, name=None, adress=None, gender=None, bday=None, age=None):
        """Edit only the fields provided"""
        if name:
            self.name = name
        if adress:
            self.adress = adress
        if gender:
            self.gender = gender
        if bday:
            self.bday = bday
        if age:
            self.age = age

        return self.getimfo()

    def __str__(self):
        """Pretty string output for debugging"""
        return f"Student(id={self.id}, name='{self.name}', gender={self.gender}, age={self.age}, adress='{self.adress}')"


# ========================================================================

Students = []


def newstudent(name, id, adress, gender, bday, age):
    """Create and store a new student"""
    if not all([name, id, adress, gender, bday, age]):
        return "Missing information"

    a = Student(
        name=name,
        id=id,
        adress=adress,
        gender=gender,
        bday=bday,
        age=age,
        joindate=time.strftime('%c')
    )
    Students.append(a)
    return a


def printstudentimfo():
    """Print all students in clean format"""
    for s in Students:
        id, name, gender, age, adress, join = s.getimfo()

        print(
            f"name     : {name}\n"
            f"id       : {id}\n"
            f"gender   : {gender}\n"
            f"age      : {age}\n"
            f"adress   : {adress}\n"
            f"joindate : {join}\n"
            f"{'-'*40}\n"
        )


def test():
    """Load initial students from stdlist"""
    for id, std in enumerate(stdlist, start=1):
        name, adress, gender, bday, age = std

        a = Student(
            name=name,
            id=id,
            adress=adress,
            gender=gender,
            bday=bday,
            age=age,
            joindate=time.strftime('%c')
        )
        Students.append(a)


if __name__ == '__main__':
    test()
    printstudentimfo()
