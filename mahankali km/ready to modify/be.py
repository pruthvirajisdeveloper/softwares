import time
import psycopg2
from psycopg2.pool import SimpleConnectionPool

# ===================== POSTGRES CONNECTION POOL ===============================

POOL = None

def init_pool():
    """Initialize PostgreSQL connection pool"""
    global POOL
    if POOL is None:
        POOL = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host="localhost",
            port=5432,
            user="postgres",
            password="",
            database="db"
        )
        print("Pool created!")


def get_conn():
    """Get a pooled connection"""
    return POOL.getconn()


def put_conn(conn):
    """Return connection to pool"""
    POOL.putconn(conn)


def init_db():
    """Create table if missing"""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            adress TEXT NOT NULL,
            gender TEXT NOT NULL,
            bday TEXT NOT NULL,
            age INT NOT NULL,
            joindate TEXT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    put_conn(conn)


# ===================== DB OPERATIONS ===============================

def db_add_student(s):
    """Insert a student using pool"""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students(name, adress, gender, bday, age, joindate)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (s.name, s.adress, s.gender, s.bday, s.age, s.joindate))

    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    put_conn(conn)
    return new_id


def db_load_students():
    """Load all students using pool"""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, adress, gender, bday, age, joindate FROM students;")
    rows = cur.fetchall()

    cur.close()
    put_conn(conn)
    return rows


# ===================== STUDENT CLASS ===============================

class Student:
    """Student structure matching DB"""
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
        return f"Student(id={self.id}, name='{self.name}', gender={self.gender}, age={self.age}, adress='{self.adress}')"


# ===================== MANAGER ===============================

Students = []

def newstudent(id, name, adress, gender, bday, age, joindate):
    """Create student + save to DB"""
    if not all([name, id, adress, gender, bday, age]):
        return "Missing information"
    s = Student(id=id, name=name, adress=adress, gender=gender, bday=bday, age=age, joindate=joindate)
    new_id = db_add_student(s)
    s.id = new_id

    Students.append(s)
    return s


def printstudentimfo():
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
    """Load real students from DB via pool"""
    init_pool()
    init_db()

    Students.clear()
    rows = db_load_students()
    for r in rows:
        id, name, adress, gender, bday, age, join = r
        Students.append(Student(name, id, adress, gender, bday, age, join))


if __name__ == "__main__":
    test()
    printstudentimfo()
