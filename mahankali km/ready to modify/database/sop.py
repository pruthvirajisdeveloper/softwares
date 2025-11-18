
from database import get_conn, put_conn
# ===================== DB OPERATIONS ===============================

def db_add_student(s):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students (name, address, gender, bday, age, joindate)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (s.name, s.address, s.gender, s.bday, s.age, s.joindate))

    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    put_conn(conn)
    return new_id


def db_load_students():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, address, gender, bday, age, joindate FROM students;")

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
        SET name=%s, address=%s, gender=%s, bday=%s, age=%s
        WHERE id=%s;
    """, (s.name, s.address, s.gender, s.bday, s.age, s.id))

    conn.commit()
    cur.close()
    put_conn(conn)
    return f'success'