class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///librarydata.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'veryverysecretkey'
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    CACHE_TYPE = 'redis'
    CASH_REDIS_URL = 'redis://localhost:6379/3'