# db.py — v2.2
# ---------------------------------------
# Database Bridge (Connection Pool Only)
# ---------------------------------------

import psycopg2
from psycopg2.pool import SimpleConnectionPool


class Bridge:
    pool = None

    @classmethod
    def init_pool(cls):
        try:
            cls.pool = SimpleConnectionPool(
                minconn=1,
                maxconn=5,
                user="postgres",
                password=9900,
                host="localhost",
                port=1234,
                database="testsql"
            )
            print("[Bridge] Connection pool ready.")
        except Exception as e:
            print("[Bridge ERROR]", e)

    @classmethod
    def get_conn(cls):
        conn = cls.pool.getconn()
        print("[Bridge] Connection checked out.")
        return conn

    @classmethod
    def return_conn(cls, conn):
        cls.pool.putconn(conn)
        print("[Bridge] Connection returned.")

    @classmethod
    def close_pool(cls):
        if cls.pool:
            cls.pool.closeall()
            print("[Bridge] All connections closed.")
