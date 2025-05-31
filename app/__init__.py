import os
import datetime
from flask import Flask, request
from flask_migrate import Migrate
from user_agents import parse

from .db import db, VisitorStats
from .model import Expense, Category  # Import your models here
from .commands import create_admin_user

# Initialize migrate outside create_app to reuse it
migrate = Migrate(render_as_batch=True)

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "NOTHING_IS_SECRET")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///master.sqlite3")
    app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=7)

    # Initialize database and migration with app
    db.init_app(app)
    migrate.init_app(app, db)

    # After each request, prevent caching for dynamic content
    @app.after_request
    def after_request_(response):
        if request.endpoint != "static":
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    # Import and register your blueprints
    from .views.auth import auth
    from .views.home import home
    from .views.settings import settings
    from .views.admin import admin

    blueprints = [auth, home, settings, admin]

    for bp in blueprints:
        app.register_blueprint(bp)

    # Track visitor stats on each request (except static files)
    @app.before_request
    def app_before_data():
        if request.endpoint != "static":
            try:
                user_agent = parse(request.user_agent.string)
                stat = VisitorStats(
                    browser=user_agent.browser.family,
                    device=user_agent.get_device(),
                    operating_system=user_agent.get_os(),
                    is_bot=user_agent.is_bot
                )
                db.session.add(stat)
                db.session.commit()
            except Exception as e:
                db.session.rollback()  # rollback session on error
                print(f"VisitorStats logging error: {e}")

    # Add CLI commands (like creating admin user)
    app.cli.add_command(create_admin_user)

    return app
