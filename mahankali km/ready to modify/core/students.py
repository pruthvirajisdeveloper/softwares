class Student:
    def __init__(self, name, age, gender, reg_number, mob_number):
        self.name = name
        self.age = age
        self.gender = gender
        self.reg_number = reg_number
        self.mob_number = mob_number

    def get_details(self):
        print(
            f"\n{self.name} : {self.gender}, {self.age} years old"
            f"\nReg. number: {self.reg_number}"
            f"\nMobile number: {self.mob_number}"
        )

    def edit_info(self, name=None, age=None, gender=None, mob_number=None):
        if name:
            self.name = name
        if age:
            self.age = age
        if gender:
            self.gender = gender
        if mob_number:
            self.mob_number = mob_number
        print(f"Student {self.reg_number} updated successfully.")

    def __str__(self):
        return f"[{self.reg_number}]: {self.name} ({self.gender}, {self.age})"
