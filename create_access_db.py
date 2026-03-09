"""
create_access_db.py
-------------------
Generates a Microsoft Access (.accdb) database for the
Event Registration & Attendance Information System.

Requirements (Windows only):
    pip install pyodbc
    Microsoft Access Database Engine must be installed:
    https://www.microsoft.com/en-us/download/details.aspx?id=54920

Usage:
    python create_access_db.py [output_path]

    output_path defaults to: event_registration.accdb
"""

import sys
import os

DB_NAME = sys.argv[1] if len(sys.argv) > 1 else "event_registration.accdb"

DDL_STATEMENTS = [
    # users
    """
    CREATE TABLE users (
        id             AUTOINCREMENT CONSTRAINT pk_users PRIMARY KEY,
        name           TEXT(255) NOT NULL,
        email          TEXT(255) NOT NULL,
        email_verified DATETIME,
        password       TEXT(255) NOT NULL,
        remember_token TEXT(100),
        created_at     DATETIME,
        updated_at     DATETIME
    )
    """,
    "CREATE UNIQUE INDEX uq_users_email ON users (email)",

    # events
    """
    CREATE TABLE events (
        id         AUTOINCREMENT CONSTRAINT pk_events PRIMARY KEY,
        title      TEXT(255) NOT NULL,
        event_date DATETIME  NOT NULL,
        event_time TEXT(20)  NOT NULL,
        location   TEXT(255) NOT NULL,
        created_at DATETIME,
        updated_at DATETIME
    )
    """,

    # registrations
    """
    CREATE TABLE registrations (
        id            AUTOINCREMENT CONSTRAINT pk_registrations PRIMARY KEY,
        event_id      LONG      NOT NULL,
        student_id    TEXT(255) NOT NULL,
        name          TEXT(255) NOT NULL,
        email         TEXT(255) NOT NULL,
        qr_token      TEXT(255) NOT NULL,
        checked_in_at DATETIME,
        created_at    DATETIME,
        updated_at    DATETIME
    )
    """,
    "CREATE UNIQUE INDEX uq_reg_qr_token ON registrations (qr_token)",
    "CREATE UNIQUE INDEX uq_reg_student  ON registrations (event_id, student_id)",
    "CREATE INDEX idx_reg_event_id ON registrations (event_id)",

    # password_reset_tokens
    """
    CREATE TABLE password_reset_tokens (
        email      TEXT(255) CONSTRAINT pk_prt PRIMARY KEY,
        token      TEXT(255) NOT NULL,
        created_at DATETIME
    )
    """,

    # sessions
    """
    CREATE TABLE sessions (
        id            TEXT(255) CONSTRAINT pk_sessions PRIMARY KEY,
        user_id       LONG,
        ip_address    TEXT(45),
        user_agent    MEMO,
        payload       MEMO NOT NULL,
        last_activity LONG NOT NULL
    )
    """,
    "CREATE INDEX idx_sessions_user_id      ON sessions (user_id)",
    "CREATE INDEX idx_sessions_last_activity ON sessions (last_activity)",

    # cache
    """
    CREATE TABLE cache (
        cache_key  TEXT(255) CONSTRAINT pk_cache PRIMARY KEY,
        value      MEMO      NOT NULL,
        expiration LONG      NOT NULL
    )
    """,

    # jobs
    """
    CREATE TABLE jobs (
        id           AUTOINCREMENT CONSTRAINT pk_jobs PRIMARY KEY,
        queue        TEXT(255) NOT NULL,
        payload      MEMO      NOT NULL,
        attempts     BYTE      NOT NULL,
        reserved_at  LONG,
        available_at LONG      NOT NULL,
        created_at   LONG      NOT NULL
    )
    """,
    "CREATE INDEX idx_jobs_queue ON jobs (queue)",
]


def create_with_pyodbc(db_path: str) -> bool:
    """Create .accdb using pyodbc + Microsoft ACE OLEDB driver (Windows)."""
    try:
        import pyodbc
    except ImportError:
        return False

    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={db_path};"
        r"CREATE_DB=YES;"
    )
    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        for ddl in DDL_STATEMENTS:
            ddl = ddl.strip()
            if ddl:
                try:
                    cursor.execute(ddl)
                except Exception as e:
                    print(f"  [warn] {e}  →  {ddl[:60]}...")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"pyodbc error: {e}")
        return False


def print_sql_fallback():
    """Print Access-compatible SQL so the user can run it manually."""
    print("\n" + "=" * 60)
    print("Microsoft ACE driver not available on this platform.")
    print("Copy the SQL below into Access Query Designer (SQL View).")
    print("=" * 60 + "\n")
    for ddl in DDL_STATEMENTS:
        ddl = ddl.strip()
        if ddl:
            print(ddl + ";\n")


def main():
    db_path = os.path.abspath(DB_NAME)
    print(f"Target database: {db_path}")

    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing database file.")

    if create_with_pyodbc(db_path):
        print(f"\n✓ Access database created successfully: {db_path}")
        print("Tables created:")
        print("  - users")
        print("  - events")
        print("  - registrations  (FK → events, unique QR token)")
        print("  - password_reset_tokens")
        print("  - sessions")
        print("  - cache")
        print("  - jobs")
    else:
        print_sql_fallback()
        sql_path = db_path.replace(".accdb", ".sql")
        with open(sql_path, "w") as f:
            for ddl in DDL_STATEMENTS:
                ddl = ddl.strip()
                if ddl:
                    f.write(ddl + ";\n\n")
        print(f"\nSQL also saved to: {sql_path}")


if __name__ == "__main__":
    main()
