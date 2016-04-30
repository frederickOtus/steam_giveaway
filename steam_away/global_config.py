import uuid

DEBUG = False
SECRET_KEY = str(uuid.uuid4())
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

