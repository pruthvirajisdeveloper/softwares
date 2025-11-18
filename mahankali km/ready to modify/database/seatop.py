from database import get_conn, put_conn

def add_member(m):
    conn = get_conn()
    cur = conn.cursor()

    # 1️⃣ Insert student (main person)
    cur.execute("""
        INSERT INTO students (name, address, gender, bday, age, joindate)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (m.name, m.address, m.gender, m.bday, m.age, m.joindate))

    student_id = cur.fetchone()[0]

    # 2️⃣ Insert member
    cur.execute("""
        INSERT INTO members (student_id, seat_id, plan_id, start_date, relation_to_student, relation_to_plan)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        student_id,
        m.seat_id,
        m.plan_id,
        m.start_date,
        m.relation_to_student,
        m.relation_to_plan
    ))

    member_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    put_conn(conn)

    return member_id


def db_load_members():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            members.id,
            students.name,
            students.address,
            members.start_date,
            members.relation_to_student,
            members.relation_to_plan,
            seats.seat_number,
            plans.duration_days,
            plans.fees,
            plans.discount
        FROM members
        LEFT JOIN students ON members.student_id = students.id
        LEFT JOIN seats ON members.seat_id = seats.id
        LEFT JOIN plans ON members.plan_id = plans.id;
    """)

    rows = cur.fetchall()
    cur.close()
    put_conn(conn)
    return rows


def db_update_member(m):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE members
        SET seat_id = %s,
            plan_id = %s,
            start_date = %s,
            relation_to_student = %s,
            relation_to_plan = %s
        WHERE id = %s;
    """, (
        m.seat_id,
        m.plan_id,
        m.start_date,
        m.relation_to_student,
        m.relation_to_plan,
        m.id
    ))

    conn.commit()
    cur.close()
    put_conn(conn)
    return "success"