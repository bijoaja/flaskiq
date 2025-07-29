from flask import Flask, Blueprint, send_from_directory, request, send_file, after_this_request, render_template
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from utils import Profiler, Middleware, Response, TenantRateLimiter
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine

db = SQLAlchemy()
rate_limiter = TenantRateLimiter()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Profiler.register_profiler(app)
    CORS(app)
    rate_limiter.init_app(app)

    # Cek dan buat database jika belum ada
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"📦 Database {engine.url.database} berhasil dibuat.")

    # Inisialisasi database & migrasi
    db.init_app(app)
    migrate = Migrate(app, db)

    # Error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # Blueprint
    from app.routes import api_bp, view_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(view_bp)

    return app

app = create_app()