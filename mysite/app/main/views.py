import datetime
import json
import numpy as np
from flask import jsonify, request, abort
from . import main
from .. import db
from ..models import load_person, add_persons, date_valid, last_import_id, recommit_person, Person, age

# при проверке на валидность времени
# datetime.date(year, month, day)
# если данные не валидны, вызывается ошибка
# обрабатывать try / except


@main.route("/imports", methods=["POST"])
def parse():
	# проверяем код на ошибки


	    json_body = request.json["citizens"]
	    import_id = last_import_id()

	    add_persons(json_body, import_id=import_id)
	    db.session.commit()
	    return "dfsf"
	# в случае ошибки 
	# except:
	# 	abort(400)

	# return jsonify({"data":{"import_id":import_id+1}}), 201


@main.route("/imports/<int:import_id>/citizens/<int:citizen_id>", methods=["PATCH"])
def reload(import_id, citizen_id):
	json_body = request.json

	last_relatives = recommit_person(json_body, import_id, citizen_id)

	try: 
		relatives = set(json.loads(json_body["relatives"]))
		last_relatives = set(last_relatives)
		value_append = relatives - last_relatives
		value_remove = last_relatives - relatives
		for i in value_append:
			js = load_person(import_id, int(i))[0]
			js.relatives = json.loads(js.relatives)
			js.relatives.append(citizen_id)
			js.relatives = str(js.relatives)
		for i in value_remove:
			js = load_person(import_id, int(i))[0]
			js.relatives = json.loads(js.relatives)
			js.relatives.remove(citizen_id)
			js.relatives = str(js.relatives)
		db.session.commit()
	except:
		pass

	result = load_person(import_id, citizen_id)[0]
	return jsonify({
		"data": {
			"citizen_id":result.citizen_id,
			"town":result.town,
			"street":result.street,
			"building":result.building,
			"apartment":result.apartment,
			"name":result.name,
			"birth_date":result.birth_date,
			"gender":result.gender,
			"relatives":result.relatives,
		}
	}), 200

@main.route("/imports/<int:import_id>/citizens", methods=["GET"])
def citizens(import_id):
	citizens = list(Person.to_dict(Person.query.filter_by(import_id=import_id).all()))
	return jsonify({"data":citizens}), 200

@main.route("/imports/<int:import_id>/citizens/birthdays", methods=["GET"])
def birthdays(import_id):
	citizens = list(Person.to_dict(Person.query.filter_by(import_id=import_id).all()))
	content = {}
	for i in citizens:
		content[i["citizen_id"]] = int(i["birth_date"].split(".")[1])
	data = {"1":{},	"2":{},	"3":{},	"4":{},	"5":{},	"6":{},	"7":{},	"8":{},	"9":{}, "10":{}, "11":{}, "12":{}}
	for i in citizens:
		relatives = json.loads(i["relatives"])
		for k in relatives:
			month = content[k]
			try:
				data[str(month)][i["citizen_id"]] += 1
			except:
				data[str(month)][i["citizen_id"]] = 1

	for m, i in data.items():
		result = []
		for k, n in i.items():
			result.append({"citizen_id":int(k), "presents":int(n)})
		data[m] = list(result)
	return jsonify(data)

@main.route("/imports/<int:import_id>/towns/stat/percentile/age", methods=["GET"])
def percentile(import_id):
	dates = {}
	# собираем возраст в data
	for i in Person.query.filter_by(import_id=import_id).all():
		try:
			dates[i.town].append(age(i.birth_date))
		except:
			dates[i.town] = [age(i.birth_date)]

	for i, k in dates.items():
		result = {"town":i}
		# вычисляем перцентили
		result["p50"] = int(np.percentile(k, 50))
		result["p75"] = int(np.percentile(k, 75))
		result["p99"] = int(np.percentile(k, 99))
		dates[i] = result

	# jsonим dates
	return jsonify(dates)