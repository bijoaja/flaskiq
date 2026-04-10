from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

from config import config
from utils import Profiler, TenantRateLimiter

db = SQLAlchemy()
migrate = Migrate()
rate_limiter = TenantRateLimiter()
csrf = CSRFProtect()


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # ── Extensions ────────────────────────────────────────────────────────────
    Profiler.register_profiler(app)
    CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", ["*"])}})
    rate_limiter.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # ── Security headers ──────────────────────────────────────────────────────
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"]        = "DENY"
        response.headers["X-XSS-Protection"]       = "1; mode=block"
        response.headers["Referrer-Policy"]         = "strict-origin-when-cross-origin"
        return response

    # ── Database initialisation ───────────────────────────────────────────────
    with app.app_context():
        db.create_all()

    # ── Error handlers ────────────────────────────────────────────────────────
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        from utils import Response
        return Response().invalid(
            is_success=False, values=None,
            message="Rate limit exceeded. Please slow down.",
            code=429,
        )

    # ── Blueprints ────────────────────────────────────────────────────────────
    from app.routes import landing_bp, auth_view_bp, cms_bp, api_v1_bp

    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_view_bp)
    app.register_blueprint(cms_bp)
    app.register_blueprint(api_v1_bp)

    # API routes use Bearer JWT — exempt from CSRF
    csrf.exempt(api_v1_bp)

    return app


app = create_app()
