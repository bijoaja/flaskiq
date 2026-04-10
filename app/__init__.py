from flask import Flask, Blueprint, send_from_directory, request, send_file, after_this_request, render_template
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config
from utils import Profiler, Middleware, Response, TenantRateLimiter
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine

db = SQLAlchemy()
migrate = Migrate()
rate_limiter = TenantRateLimiter()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])
    Profiler.register_profiler(app)
    CORS(app)
    rate_limiter.init_app(app)

    # Initialize  database & migration
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # Error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # Register Blueprints
    from app.routes import api_v1_bp, view_bp
    app.register_blueprint(api_v1_bp)
    app.register_blueprint(view_bp)

    return app

app = create_app()