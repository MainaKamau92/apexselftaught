"""Api configurations"""
import os


class Config:
    """
    Base configuration class.
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY =  os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Testing Configurations, with a separate test database
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """
    Staging configuartions
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
