"""Api configurations"""
import os


class Config:
    """
    Base configuration class.
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')


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
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL')
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
