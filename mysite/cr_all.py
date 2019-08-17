from flask import Flask
from app.models import last_import_id
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mypassword@localhost:3306/tests"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

association_table = db.Table("association",
    db.Column("import_id", db.Integer, primary_key=True, default=last_import_id),
    db.Column("persons_citizen_id", db.Integer, db.ForeignKey("persons.citizen_id"), primary_key=True), 
    # db.Column("persons_import_id", db.Integer, db.ForeignKey("persons.import_id")), 
    db.Column("relatives_citizen_id", db.Integer, db.ForeignKey("relatives.citizen_id"), primary_key=True),)
    # db.Column("relatives_import_id", db.Integer, db.ForeignKey("relatives.import_id")))


class Person(db.Model):

    # структура таблицы
    # была ранее использована для её создания

    __tablename__ = "persons"
    import_id = db.Column(db.Integer)
    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String(64), nullable=False)
    street = db.Column(db.String(80), nullable=False)
    building = db.Column(db.String(64), nullable=False)
    apartment = db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    relative = db.relationship("Relative",
                        secondary=association_table, backref=db.backref('persons', lazy="dynamic"))
    db.PrimaryKeyConstraint(citizen_id, import_id)

    # конструктор
    # нужен для удобной записи данных в таблицу
    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)

class Relative(db.Model):
    __tablename__ = "relatives"
    id = db.Column(db.Integer, autoincrement=True)
    import_id = db.Column(db.Integer)
    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String(64), nullable=False)
    street = db.Column(db.String(80), nullable=False)
    building = db.Column(db.String(64), nullable=False)
    apartment = db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    # relative = db.relationship("Relatives",
    #                 secondary=association_table, backref=db.backref('persons', lazy="dynamic"))
    db.PrimaryKeyConstraint(citizen_id, id, import_id)

    def __init__(self, **kwargs):
        super(Relative, self).__init__(**kwargs)