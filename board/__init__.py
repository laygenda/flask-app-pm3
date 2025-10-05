# board/__init__.py
import os
from dotenv import load_dotenv
from flask import Flask

from board import pages, posts, database

load_dotenv()

def create_app():
    # Mengatur instance_relative_config=True sangat penting untuk SQLite
    # agar file db disimpan di direktori 'instance'
    app = Flask(__name__, instance_relative_config=True) 

    # --- PERBAIKAN: SET DEFAULT CONFIG ---
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        # Mengatur default DATABASE path ke instance/sqlite.db
        DATABASE=os.path.join(app.instance_path, "sqlite.db"), 
    )
    
    # Memuat konfigurasi dari environment (akan menimpa nilai default di atas)
    app.config.from_prefixed_env()

    # Pastikan direktori instance ada, diperlukan untuk menyimpan file SQLite
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # -------------------------------------

    database.init_app(app)

    app.register_blueprint(pages.bp)
    app.register_blueprint(posts.bp)

    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    print(f"Using Database: {app.config.get('DATABASE')}")
    return app
