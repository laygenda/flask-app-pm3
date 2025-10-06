import psycopg2
from flask import g

# --- Konfigurasi Koneksi PostgreSQL untuk Docker Compose ---
# Kunci ini **wajib** sama dengan yang ada di docker-compose.yml
DB_CONFIG = {
    "host": "psql-db",       
    "database": "flask_db",
    "user": "admin",
    "password": "P4ssw0rd",
    "port": "5432"
}

def get_pg_db_conn():
    """Membuka koneksi PostgreSQL menggunakan DB_CONFIG."""
    # Pastikan koneksi disimpan di g
    if "pg_conn" not in g:
        try:
            # Psycopg2.connect menerima KEYWORD ARGUMENTS (**DB_CONFIG)
            g.pg_conn = psycopg2.connect(**DB_CONFIG)
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            # Naikkan error agar Flask tahu bahwa ada masalah
            raise
    return g.pg_conn

def close_pg_db_conn(e=None):
    """Menutup koneksi PostgreSQL jika ada di g."""
    pg_conn = g.pop("pg_conn", None)

    if pg_conn is not None:
        pg_conn.close()

def init_app(app):
    """Mendaftarkan fungsi penutup koneksi."""
    app.teardown_appcontext(close_pg_db_conn)

