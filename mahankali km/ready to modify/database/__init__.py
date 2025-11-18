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
            database="library"
        )
        print("Pool created!")


def get_conn():
    global POOL
    return POOL.getconn()


def put_conn(conn):
    global POOL
    POOL.putconn(conn)

