from . import db

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

# возвращает предыдущий import_id
# чтоб не было никаких проблем с auto_increment
def last_import_id():
    import_ids = Birthday.query.filter(Birthday.id).all()
    if import_ids:
        return import_ids[-1].import_id
    else:
        return 0

