
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Houston1987!@localhost/mechanic_db'
    DEBUG = True # Causes flask app to auto update on code changes

    class TestingConfig:
        pass

    class ProductionConfig:
        pass
    