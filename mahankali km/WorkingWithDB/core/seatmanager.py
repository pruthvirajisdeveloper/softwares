
from db import Bridge
# === SEATS ===
class SeatManager:
    def add(self, seat_number, status='available'):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO seats (seat_number, status)
                VALUES (%s, %s);
            """, (seat_number, status))
            conn.commit()
            print(f"[DB] Seat added → {seat_number}")
        except Exception as e:
            print("[DB ERROR: SeatManager.add]", e)
            conn.rollback()
        finally:
            cur.close()
            Bridge.return_conn(conn)

    def list(self):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, seat_number, status FROM seats ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        Bridge.return_conn(conn)
        return rows

    def add_day(self, seat_number, status='available'):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO seats_day (seat_number, status)
                VALUES (%s, %s);
            """, (seat_number, status))
            conn.commit()
            print(f"[DB] Seat (Day) added → {seat_number}")
        except Exception as e:
            print("[DB ERROR: SeatManager.add_day]", e)
            conn.rollback()
        finally:
            cur.close()
            Bridge.return_conn(conn)

    def add_night(self, seat_number, status='available'):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO seats_night (seat_number, status)
                VALUES (%s, %s);
            """, (seat_number, status))
            conn.commit()
            print(f"[DB] Seat (Night) added → {seat_number}")
        except Exception as e:
            print("[DB ERROR: SeatManager.add_night]", e)
            conn.rollback()
        finally:
            cur.close()
            Bridge.return_conn(conn)

    def list_day(self):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, seat_number, status FROM seats_day ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        Bridge.return_conn(conn)
        return rows

    def list_night(self):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, seat_number, status FROM seats_night ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        Bridge.return_conn(conn)
        return rows
