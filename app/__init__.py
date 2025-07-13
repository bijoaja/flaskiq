from flask import Flask, Blueprint, send_from_directory, request, send_file, after_this_request, render_template
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from utils import Profiler, Middleware, Response, TenantRateLimiter

db = SQLAlchemy()

rate_limiter = TenantRateLimiter()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Profiler.register_profiler(app)

    CORS(app)
    
    # limiter.init_app(app)
    rate_limiter.init_app(app)
    
    # Register Routes and other module
    from app.routes import api_bp, view_bp
    
    # Inisialisasi Database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
    

    app.register_blueprint(api_bp)
    app.register_blueprint(view_bp)

    return app


app = create_app()
