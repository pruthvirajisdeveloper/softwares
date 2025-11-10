# --- Optional: Drop old tables before recreate (Dev only) ---
# cur.execute("""
#     DROP TABLE IF EXISTS student_history, seat_history, bookings,
#     payments, seats_night, seats_day, seats, plans, students CASCADE;
# """)
# print("[DB] Old tables dropped (Dev Mode).\n")


from db import Bridge
import traceback

def create_all_tables():
    """Create all tables required for the system."""
    conn = Bridge.get_conn()
    cur = conn.cursor()
    # --- Optional: Drop old tables before recreate (Dev only) ---
    # (All drop statements removed as requested)
    try:
        # 1️⃣ Students Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT,
                gender TEXT CHECK (gender IN ('M', 'F', 'Other')),
                birth_date DATE,
                reg_number TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("[DB] Table 'students' ready.\n")

        # 2️⃣ Plans Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                shift TEXT CHECK (shift IN ('Morning', 'Evening', 'Night')),
                days INTEGER NOT NULL,
                price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (name, shift, days, price)
            );
        """)
        print("[DB] Table 'plans' ready.\n")

        # 3️⃣ Seats Table (Day Shift)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS seats_day (
                id SERIAL PRIMARY KEY,
                seat_number TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'available' CHECK (status IN ('available', 'occupied', 'reserved', 'maintenance')),
                student_id INTEGER REFERENCES students(id),
                plan_id INTEGER REFERENCES plans(id),
                start_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("[DB] Table 'seats_day' ready.\n")

        # 4️⃣ Seats Table (Night Shift)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS seats_night (
                id SERIAL PRIMARY KEY,
                seat_number TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'available' CHECK (status IN ('available', 'occupied', 'reserved', 'maintenance')),
                student_id INTEGER REFERENCES students(id),
                plan_id INTEGER REFERENCES plans(id),
                start_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("[DB] Table 'seats_night' ready.\n")

        # 5️⃣ Payments Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id) ON DELETE SET NULL,
                method TEXT CHECK (method IN ('Cash', 'UPI', 'Online')),
                amount REAL NOT NULL,
                details TEXT,
                seat_id INTEGER NOT NULL,
                seat_table TEXT CHECK (seat_table IN ('seats_day', 'seats_night')) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("[DB] Table 'payments' ready.\n")

        # 6️⃣ Seat History Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS seat_history (
                id SERIAL PRIMARY KEY,
                seat_id INTEGER NOT NULL,
                seat_table TEXT CHECK (seat_table IN ('seats_day', 'seats_night')) NOT NULL,
                student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
                action TEXT NOT NULL,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session TEXT
            );
        """)
        print("[DB] Table 'seat_history' ready.\n")

        # 7️⃣ Student History Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student_history (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
                seat_history_id INTEGER REFERENCES seat_history(id) ON DELETE CASCADE,
                remark TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("[DB] Table 'student_history' ready.\n")

        # 8️⃣ Future Bookings Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
                seat_id INTEGER NOT NULL,
                seat_table TEXT CHECK (seat_table IN ('seats_day', 'seats_night')) NOT NULL,
                plan_id INTEGER REFERENCES plans(id) ON DELETE CASCADE,
                status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'canceled')),
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                start_date DATE,
                expiry_date DATE
            );
        """)
        print("[DB] Table 'bookings' ready.\n")

        # Print table summary
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = [r[0] for r in cur.fetchall()]
        print("[DB] Tables in database:", tables, "\n")

    except Exception as e:
        print("[DB ERROR]", e)
        traceback.print_exc()
        conn.rollback()

    finally:
        conn.commit()  # ✅ ensure schema is visible
        cur.close()
        Bridge.return_conn(conn)
