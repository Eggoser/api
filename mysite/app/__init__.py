from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys

db = SQLAlchemy()

def create_app(config):
	# настройка и инициализация приложения
	app = Flask(__name__)
	app.config.from_object(config)

	if len(sys.argv) > 1 and sys.argv[1] == "runtest":
		app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mypassword@localhost:3306/flask"


	# инициализация flask пакетов
	db.init_app(app)

	# регистрация блюпринтов
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app