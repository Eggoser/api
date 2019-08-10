from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DefaultConfig

app = Flask(__name__)
app.config.from_object(DefaultConfig)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mypassword@localhost:3306/flasky"

db = SQLAlchemy(app)

# таблица для хранения json 
# информации о человеке
class Person(db.Model):

    # структура таблицы
    # была ранее использована для её создания

    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    import_id = db.Column(db.Integer)
    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String(64))
    street = db.Column(db.String(80))
    building = db.Column(db.String(80))
    apartment = db.Column(db.Integer)
    birth_date = db.Column(db.String(80))
    name = db.Column(db.Text)
    gender = db.Column(db.String(64))
    relatives = db.Column(db.Text)
