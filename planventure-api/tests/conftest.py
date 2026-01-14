"""
Shared pytest configuration and fixtures
"""
import os
import pytest
from app import app, db


@pytest.fixture(scope='session')
def test_app():
    """Create application for testing."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app


@pytest.fixture
def client(test_app):
    """Create test client."""
    with test_app.app_context():
        db.create_all()
        yield test_app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def runner(test_app):
    """Create CLI test runner."""
    return test_app.test_cli_runner()
