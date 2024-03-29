from . import db

# таблица для хранения json 
# информации о человеке
class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.JSON, nullable=False)

    # для удобной записи существует конструктор
    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)

class Birthday(db.Model):
    __tablename__ = "birthdays"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.JSON, nullable=False)

    # для удобной записи существует конструктор
    def __init__(self, **kwargs):
        super(Birthday, self).__init__(**kwargs)

class Percentile(db.Model):
    __tablename__ = "percentiles"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.JSON, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    # для удобной записи существует конструктор
    def __init__(self, **kwargs):
        super(Percentile, self).__init__(**kwargs)

class Bool(db.Model):
    __tablename__ = "booleans"
    id = db.Column(db.Integer, primary_key=True)
    birthday_bool = db.Column(db.Boolean, nullable=False)
    percentile_bool = db.Column(db.Boolean, nullable=False)

    # для удобной записи существует конструктор
    def __init__(self, **kwargs):
        super(Bool, self).__init__(**kwargs)
