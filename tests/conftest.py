import os
import pytest
from app import create_app
from app.models import db, User

@pytest.fixture
def app():
    # Override env vars for testing
    os.environ['FLASK_ENV'] = 'development'
    os.environ['DATABASE_URL'] = 'sqlite:///test_todo.db'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['WTF_CSRF_ENABLED'] = 'False' # Disable CSRF for easier testing

    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "WTF_CSRF_CHECK_DEFAULT": False,
        "LOGIN_DISABLED": False
    })

    # Setup test DB
    with app.app_context():
        db.create_all()

    yield app

    # Teardown test DB
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        user1 = User(username="user1", password_hash="hashed_pw")
        user2 = User(username="user2", password_hash="hashed_pw")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
