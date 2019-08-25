import os

class DefaultConfig:
	SECRET_KEY = "d34d(2e#d21*dfsq/dflnhjpo]20-mh/b,ghlsqmckr3i4f"
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@localhost:3306/flask".format(os.environ.get("DATABASE_USER") or "root", os.environ.get("DATABASE_PASSWORD") or "mypassword")
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TESTING = True
	JSON_AS_ASCII = False
