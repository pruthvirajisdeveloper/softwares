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
            port=1234,
            user="postgres",
            password="9900",
            database="studentsdb2"
        )
        print("Pool created!")


def get_conn():
    return POOL.getconn()


def put_conn(conn):
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
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students (name, adress, gender, bday, age, joindate)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (s.name, s.adress, s.gender, s.bday, s.age, s.joindate))

    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    put_conn(conn)
    return new_id


def db_load_students():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, adress, gender, bday, age, joindate FROM students;")
    rows = cur.fetchall()

    cur.close()
    put_conn(conn)
    return rows


def db_update_student(s):
    """Update DB row from Student object"""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE students
        SET name=%s, adress=%s, gender=%s, bday=%s, age=%s
        WHERE id=%s;
    """, (s.name, s.adress, s.gender, s.bday, s.age, s.id))

    conn.commit()
    cur.close()
    put_conn(conn)


# ===================== STUDENT CLASS ===============================

class Student:
    def __init__(self, id, name, adress, gender, bday, age, joindate):
        self.id = id
        self.name = name
        self.adress = adress
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
            self.adress,
            self.bday,
            self.joindate,
        ]

    def update(self):
        """Update database"""
        db_update_student(self)

    def __str__(self):
        return f"Student(id={self.id}, name='{self.name}', gender={self.gender}, age={self.age}, adress='{self.adress}')"


# ===================== MANAGER ===============================

Students = []

def newstudent(id, name, adress, gender, bday, age, joindate):
    if not all([name, adress, gender, bday, age]):
        return "Missing information"

    s = Student(id=id, name=name, adress=adress, gender=gender, bday=bday, age=age, joindate=joindate)
    new_id = db_add_student(s)
    s.id = new_id

    Students.append(s)
    return s


def printstudentimfo():
    for s in Students:
        id, name, gender, age, adress, join = s.getimfo()[:6]
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
    init_pool()
    init_db()

    Students.clear()
    rows = db_load_students()

    for r in rows:
        id, name, adress, gender, bday, age, join = r
        Students.append(Student(id, name, adress, gender, bday, age, join))


if __name__ == "__main__":
    test()
    printstudentimfo()
