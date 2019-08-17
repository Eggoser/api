from . import db
import datetime
from dateutil.relativedelta import relativedelta
from json import loads

# таблица для хранения 
# exec("Person_{} = type('Mai'.title(), (Person, db.Model), { '__tablename__' : 'table_{}' }, {'town':db.Column(db.String(64))}, {'street':db.Column(db.String(64))}, {'building':db.Column(db.String(64))}, {'apartment':db.Column(db.Integer)}, {'birth_date' db.Column(db.DateTime)}, {'name':db.Column(db.Text)}, {'gender':db.Column(db.String(8))}, {'children':db.relationship('Relatives',secondary=association_table, backref=db.backref('persons', lazy=True))})".format(next_value, next_value))


# возвращает предыдущий import_id
def last_import_id():
    import_ids = Person.query.filter(Person.import_id).all()
    if import_ids:
        return import_ids[-1].import_id + 1
    else:
        return 1

def last_import_id_association():
    import_ids = Person.query.filter(Person.import_id).all()
    if import_ids:
        return import_ids[-1].import_id
    else:
        return 1

# информации о человеке
association_table = db.Table("association",
    db.Column("import_id", db.Integer, primary_key=True, default=last_import_id_association),
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

    # вызывается для dict представления
    def to_dict(obj_1):
        for obj in obj_1:
            yield {
                    "citizen_id":obj.citizen_id, 
                    "town":obj.town, 
                    "street":obj.street, 
                    "buiding":obj.building,
                    "apartment":obj.apartment, 
                    "birth_date":obj.birth_date, 
                    "name":obj.name, 
                    "gender":obj.gender}

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
    db.PrimaryKeyConstraint(citizen_id, id, import_id)

    def __init__(self, **kwargs):
        super(Relative, self).__init__(**kwargs)





# Выгрузка пользователя из db
def load_person(import_id=None, citizen_id=None):
    if import_id and citizen_id:
        return Person.query.filter_by(import_id=int(import_id), citizen_id=int(citizen_id)).all()
    if import_id:
        return Person.query.filter_by(import_id=int(import_id)).all()

    if citizen_id:
        return Person.query.filter_by(import_id=int(citizen_id)).all()



# загрузка пользователя в db
def add_persons(json_body, import_id=1, citizen_id=0):
    relatives = dict((i["citizen_id"], i["relatives"]) for i in json_body)
    for obj in json_body:
        human = Person(citizen_id=int(citizen_id) or int(obj["citizen_id"]),
                    import_id=int(import_id),
                    town=str(obj["town"]),
                    street=str(obj["street"]),
                    building=str(obj["building"]),
                    apartment=int(obj["apartment"]),
                    birth_date=date_valid(obj["birth_date"]),
                    name=str(obj["name"]),
                    gender=str(obj["gender"]), age=2)

        for i in relatives[obj["citizen_id"]]:
            relativ = Relative(citizen_id=i,
                                import_id=int(import_id),
                                town=str(obj["town"]),
                                street=str(obj["street"]),
                                building=str(obj["building"]),
                                apartment=int(obj["apartment"]),
                                birth_date=date_valid(obj["birth_date"]),
                                name=str(obj["name"]),
                                gender=str(obj["gender"]), age=2)
            human.relative.append(relativ)

            # for k in relatives[i]:
            #     person = Person(citizen_id=k,
            #                     import_id=int(import_id),
            #                     town=str(obj["town"]),
            #                     street=str(obj["street"]),
            #                     building=str(obj["building"]),
            #                     apartment=int(obj["apartment"]),
            #                     birth_date=date_valid(obj["birth_date"]),
            #                     name=str(obj["name"]),
            #                     gender=str(obj["gender"]), age=2)
            #     person.relative.append(person)



        db.session.add(human)

# def commit_relative(obj, import_id=1)

# проверяет дату на валидность
def date_valid(birth_date):
    birth_date = list(map(int, birth_date.split(".")))
    birth_date.reverse()
    try:
        return datetime.date(*birth_date)
    except:
        return True

# обновляет информацию о человеке
def recommit_person(obj_2, import_id=1, citizen_id=0):
    obj = Person.query.filter_by(import_id=import_id, citizen_id=citizen_id).first()
    try:
        obj_2["relatives"] = str(obj_2["relatives"])
    except:
        pass

    last_relatives = set(loads(obj.relatives))
    for i in obj_2:
        # функции exec и eval конечно не всегда хороши, но здесь вроде уместно
        exec("obj.{} = obj_2['{}']".format(str(i), str(i)))

    db.session.commit()
    return last_relatives

# принимает дату возвращает число полных лет
def age(date):
    today = datetime.date.today()
    age = relativedelta(today, date)
    return age.years