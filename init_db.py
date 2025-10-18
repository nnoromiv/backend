import os
from sqlalchemy import text
from db.connection import engine

SQL_FILES = ["index.sql", "incident.sql"]

def run_sql_file(path):
    with engine.connect() as conn:
        with open(path, "r") as f:
            sql_file = f.read()
        # Split statements and execute one by one
        statements = [stmt.strip() for stmt in sql_file.split(";") if stmt.strip()]
        for stmt in statements:
            conn.execute(text(stmt))  # wrap in text()
        conn.commit()  # commit changes

def init_db():
    print("⏳ Creating tables...")
    for sql_file in SQL_FILES:
        sql_path = os.path.join(os.path.dirname(__file__), sql_file)
        run_sql_file(sql_path)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    init_db()
