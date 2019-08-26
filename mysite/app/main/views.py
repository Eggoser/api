from sqlalchemy.orm.attributes import flag_modified
import datetime
from json import loads
from ..compile_c.main import validate_json, mypercentile, mybirthdays, recommit_data
from flask import jsonify, request, abort
from . import main
from .. import db
from ..models import Person, Birthday, Percentile, Bool

# при проверке на валидность времени
# datetime.date(year, month, day)
# если данные не валидны, вызывается исключение
# обрабатывать try / except


@main.route("/imports", methods=["POST"])
def parse():
	# проверяем код на ошибки
	try:
	    json_body = request.json["citizens"]
	    if validate_json(json_body):
	    	abort(400)
	    persons = Person(value={"citizens":json_body})
	    birthdays = Birthday(value=mybirthdays(json_body))
	    percentiles = Percentile(value=mypercentile(json_body, list(datetime.datetime.now().timetuple())[0:3]), date=datetime.datetime.now())
	    booleans = Bool(birthday_bool=False, percentile_bool=False)
	    db.session.add(percentiles)
	    db.session.add(birthdays)
	    db.session.add(persons)
	    db.session.add(booleans)
	    db.session.commit()
	# в случае ошибки 
	except:
		abort(400)

	return jsonify({"data":{"import_id":persons.id}}), 201


@main.route("/imports/<int:import_id>/citizens/<int:citizen_id>", methods=["PATCH"])
def reload(import_id, citizen_id):
	# ошибка может возникнуть всегда
	try:
		json_body = request.json
		citizens = Person.query.get(import_id)

		try: 
			citizens.value, result = recommit_data(json_body, citizens.value["citizens"], citizen_id)
			if validate_json(citizens.value["citizens"]):
				abort(400)
			flag_modified(citizens, "value")
			db.session.commit()
		except:
			abort(400)
		booleans = Bool.query.get(import_id)
		if "relatives" in json_body.keys():
			booleans.birthday_bool = True
		if "town" in json_body.keys():
			booleans.percentile_bool = True
		if "birth_date" in json_body.keys():
			booleans.percentile_bool = True
			booleans.birthday_bool = True

		db.session.commit()
		return jsonify(result), 200
	# если ошибка
	except:
		abort(400)


# за счет умной валидации и обработки, на get запросы не нужно ничего подсчитывать
# просто и элементарно достаем данные из соответствующих таблиц
@main.route("/imports/<int:import_id>/citizens", methods=["GET"])
def citizens(import_id):
	return jsonify(Person.query.get(import_id).value), 200

@main.route("/imports/<int:import_id>/citizens/birthdays", methods=["GET"])
def birthdays(import_id):
	try:
		birthdays = Birthday.query.get(import_id)
		booleans = Bool.query.get(import_id)

		if not booleans.birthday_bool:
			return jsonify(birthdays.value), 200

		persons = Person.query.get(import_id)
		birthdays.value = mybirthdays(persons.value["citizens"])
		booleans.birthday_bool = False
		flag_modified(birthdays, "value")

		db.session.commit()

		return jsonify(birthdays.value), 200
	except:
		abort(404)

@main.route("/imports/<int:import_id>/towns/stat/percentile/age", methods=["GET"])
def percentile(import_id):
	try:
		data = Percentile.query.get(import_id)
		booleans = Bool.query.get(import_id)

		# свежи ли данные? Они должны быть сегодняшними
		if data.date.date() == datetime.datetime.now().date() and not booleans.percentile_bool:
			return jsonify(data.value), 200

		# в связи с изменениями даты, приходиться перепроверить кому сколько лет
		data.value = mypercentile(Person.query.get(import_id).value["citizens"], list(datetime.datetime.now().timetuple())[0:3])
		data.date = datetime.datetime.now()
		booleans.percentile_bool = False
		flag_modified(data, "value")

		# обновим их в mysql
		db.session.commit()
		return jsonify(data.value), 200
	except:
		abort(404)