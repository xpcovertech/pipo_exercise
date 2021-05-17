import os
from tempfile import mkdtemp
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    DEVELOPMENT = False
    TEMPLATES_AUTO_RELOAD = True
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SECRET_KEY = os.getenv("SECRET_KEY", "secret12345")

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
	TESTING = True