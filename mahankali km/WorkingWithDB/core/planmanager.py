from db import Bridge

# === PLANS ===
class PlanManager:
    def add(self, name, shift, days, price):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO plans (name, shift, days, price)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name, shift, days, price) DO NOTHING;
            """, (name, shift, days, price))
            conn.commit()
            print(f"[DB] Plan added → {name}")
        except Exception as e:
            print("[DB ERROR: PlanManager.add]", e)
            conn.rollback()
        finally:
            cur.close()
            Bridge.return_conn(conn)

    def list(self):
        conn = Bridge.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, shift, days, price FROM plans ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        Bridge.return_conn(conn)
        return rows

