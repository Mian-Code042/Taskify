import os
from dotenv import load_dotenv
from flask import Flask
from app.models import db, User
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-replace-in-prod-very-long-string')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT Setup
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-super-secret-key-replace-in-prod')

    db.init_app(app)
    
    # Security Initializations
    csrf.init_app(app)
    limiter.init_app(app)
    
    csp = {
        'default-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://cdn.jsdelivr.net',
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com'
        ]
    }
    
    # Only enforce HTTPS and HSTS in production to avoid local dev issues
    if os.environ.get('FLASK_ENV') == 'production':
        Talisman(app, content_security_policy=csp)
    else:
        # Relaxed config for local development
        Talisman(app, force_https=False, session_cookie_secure=False, content_security_policy=csp)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    jwt = JWTManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes import main
    from app.api import api_bp
    
    app.register_blueprint(main)
    # Exempt API from CSRF as it uses JWTs
    csrf.exempt(api_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
