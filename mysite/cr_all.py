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
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.JSON, nullable=False)

    # для удобной записи существует конструктор
    def __init__(self, **kwargs):
        super(self, Person).__init__(**kwargs)

class Birthday(db.Model):
    __tablename__ = "birthdays"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.JSON, nullable=False)

    # для удобной записи существует конструктор
    def __init__(self, **kwargs):
        super(self, Birthday).__init__(**kwargs)

class Percentile(db.Model):
    __tablename__ = "percentiles"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.JSON, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    # для удобной записи существует конструктор
    def __init__(self, **kwargs):
        super(self, Percentile).__init__(**kwargs)

class Bool(db.Model):
    __tablename__ = "booleans"
    id = db.Column(db.Integer, primary_key=True)
    birthday_bool = db.Column(db.Boolean, nullable=False)
    percentile_bool = db.Column(db.Boolean, nullable=False)

    # для удобной записи существует конструктор
    def __init__(self, **kwargs):
        super(self, Bool).__init__(**kwargs)