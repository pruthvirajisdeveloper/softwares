class Library:
    def __init__(self):
        pass

class Person():
    def __init__(self, name, age, reg_number, mob_number):
        self.name=name
        self.age=age
        self.reg_number=reg_number
        self.mob_number=mob_number

class Member(Person):
    def __init__(self, name, age, reg_number, mob_number):
        super().__init__(name, age, reg_number, mob_number)
        

        

class App:
    def __init__(self):
        pass