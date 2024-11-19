import os

class Config:
    """Base configuration."""
    DEBUG = os.getenv('FLASK_DEBUG', False)  # Default: False
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoid overhead

    # Database URI: Defaults to production database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev.db')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False  # Ensure debug is off in production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True  # Enables testing mode
    DEBUG = True  # Debugging is helpful during tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
