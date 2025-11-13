import time
class Student:
    def __init__(self, name, id, adress, gender, bday, age, joindate):
        self.name=name
        self.id=id
        self.adress=adress
        self.gender=gender
        self.bday=bday
        self.age=age
        self.joindate=joindate
        
        
    def getimfo(self):
        return [
            self.id,
            self.name,
            self.gender,
            self.age,
            self.adress,
            self.joindate
            ]
    

    def edit(self, name, adress, gender, bday, age):
        if name:
            self.name=name
        if adress:
            self.adress=adress
        if gender:
            self.gender=gender
        if bday:
            self.bday=bday
        if age:
            self.age=age
        return f'{self.getimfo()}'
    

    def __str__(self):
        return (self.id, self.name, self.gender, self.age, self.adress)
        #(3, "Kripa", "Female", 18, "SA")

















'''=========================================================================================='''
stdlist=[
    [
        'sujal',
        'KE',
        'male',
        '12-12-2007',
        '0'
        ],
    [
        'Vishu',
        'MP',
        'male',
        '10-10-2007',
        '0'
        ],    
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],

    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ],
    [
        'kripa',
        'Sa',
        'female',
        '12-11-2006',
        '0'
        ]
]

Students=[]



def printstudentimfo():
    for s in Students:
        a=s.getimfo()

        print(
            f'name: {a[1]}\nid={a[0]}\ngender: {a[2]}\nage: {a[3]}\nadress: {a[4]}\njoindate: {a[5]}\n\n\n\n'
            )


def test():
    for id, std in enumerate (stdlist, start=1):
        a=Student(
            name=std[0],
            id=id,
            adress=std[1],
            gender=std[2],
            bday=std[3],
            age=std[4],
            joindate=time.strftime('%c')
            )
        Students.append(a)

if __name__=='__main__':
    test()
    printstudentimfo()