from database import get_conn, put_conn

def init_db():
    """Create all tables if missing"""
    conn = get_conn()
    cur = conn.cursor()

    # ===================== STUDENTS =====================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            gender TEXT NOT NULL,
            bday TEXT NOT NULL,
            age INT NOT NULL,
            joindate TEXT NOT NULL
        );
    """)

    # ===================== PLANS =====================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS plans(
            id SERIAL PRIMARY KEY,
            duration_days INT NOT NULL,
            fees INT NOT NULL,
            discount INT DEFAULT 0
        );
    """)

    # ===================== SEATS =====================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS seats(
            id SERIAL PRIMARY KEY,
            seat_number INT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'   -- active, booked, will_empty
        );
    """)

    # ===================== MEMBERS =====================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS members(
            id SERIAL PRIMARY KEY,

            student_id INT NOT NULL
                REFERENCES students(id)
                ON DELETE CASCADE,

            seat_id INT
                REFERENCES seats(id)
                ON DELETE SET NULL,

            plan_id INT
                REFERENCES plans(id)
                ON DELETE SET NULL,

            start_date TEXT NOT NULL,
            relation_to_student TEXT NOT NULL,
            relation_to_plan TEXT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    put_conn(conn)

if __name__ == '__main__':
    
    init_db()