from db import Bridge
class StudentManager:
    def add(self, name, address, gender, birth_date, reg_number):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO students (name, address, gender, birth_date, reg_number)
                VALUES (%s, %s, %s, %s, %s);
            """, (name, address, gender, birth_date, reg_number))
            conn.commit()
            print(f"[DB] Student added → {name}")
        except Exception as e:
            print("[DB ERROR: StudentManager.add]", e)
            conn.rollback()
        finally:
            cur.close()
            Bridge.return_conn(conn)

    def list(self):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, reg_number, gender FROM students ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        Bridge.return_conn(conn)
        return rows