from . import db
import datetime
from dateutil.relativedelta import relativedelta
from json import loads

# таблица для хранения 
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
                    "gender":obj.gender, 
                    "relatives":obj.relatives }
    # конструктор
    # нужен для удобной записи данных в таблицу
    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)




# Выгрузка пользователя из db
def load_person(import_id=None, citizen_id=None):
    if import_id and citizen_id:
        return Person.query.filter_by(import_id=int(import_id), citizen_id=int(citizen_id)).all()
    if import_id:
        return Person.query.filter_by(import_id=int(import_id)).all()

    if citizen_id:
        return Person.query.filter_by(import_id=int(citizen_id)).all()

# возвращает предыдущий import_id
def last_import_id():
    import_ids = Person.query.filter(Person.import_id).all()
    if import_ids:
        return import_ids[-1].import_id
    else:
        return 0

# загрузка пользователя в db
def commit_person(obj, import_id=1, citizen_id=0):
    human = Person(citizen_id=int(citizen_id) or int(obj["citizen_id"]),
                import_id=int(import_id + 1),
                town=str(obj["town"]), 
                street=str(obj["street"]), 
                building=str(obj["building"]),
                apartment=int(obj["apartment"]),
                birth_date=str(obj["birth_date"]),
                name=str(obj["name"]),
                gender=str(obj["gender"]),
                relatives=str(obj["relatives"]))
    db.session.add(human)

# проверяет дату на валидность
def date_valid(birth_date):
    birth_date = list(map(int, birth_date.split(".")))
    birth_date.reverse()
    try:
        datetime.date(*birth_date)
        return False
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
    f = list(map(int, date.split(".")))
    f.reverse()
    today = datetime.date.today()
    date = datetime.date(*f)
    age = relativedelta(today, date)
    return age.years