
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Houston1987!@localhost/mechanic_db'
    DEBUG = True # Causes flask app to auto update on code changes
    CACHE_TYPE = 'SimpleCache' # Use simple in-memory cache for development
    CACHE_DEFAULT_TIMEOUT = 300

    class TestingConfig:
        pass

    class ProductionConfig:
        pass
    
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
