cdef date_valid(str date):
	cdef list birth_date = []
	cdef dict months_days
	for i in date.split("."):
		birth_date.append(int(i))
	try:
		if birth_date[2] % 4 == 0:
			months_days = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
		else:
			months_days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
		if months_days[birth_date[1]] >= birth_date[0]:
			return False
		else:
			return True
	except:
		return True

cpdef validate_json(list json_body):
	cdef dict relatives = {}
	cdef i
	cdef int citizen
	cdef k
	cdef result
	try:
		for i in json_body:
			result = {}
			for k in i["relatives"]:
				result[k] = k
			relatives[i["citizen_id"]] = result
		if len(json_body) < 1:
			return True
		for i in json_body:
			if i["town"] == None or i["street"] == None or i["name"] == None or i["building"] == None or int(i["apartment"]) == 1 or i["apartment"] == None:
				return True

			if date_valid(i["birth_date"]):
				return True

			if i["gender"] != "male" and i["gender"] != "female":
				return True

			citizen = i["citizen_id"]

			for k in i["relatives"]:
				try:
					relatives[k][citizen]
				except:
					return True
		return False
	except:
		return True



import numpy as np

cdef age(str date, list now):
	cdef list birth_date = []
	cdef int age
	for i in date.split("."):
		birth_date.append(int(i))
	birth_date.reverse()
	if birth_date[1] < now[1]:
		age = now[0] - birth_date[0]

	elif birth_date[1] == now[1]:
		if birth_date[2] <= now[2]:
			age = now[0] - birth_date[0]
		else:
			age = now[0] - birth_date[0] - 1
	else:
		age = now[0] - birth_date[0] - 1
	return age

cdef datess(list array, list date):
	cdef dict dates = {}
	for i in array:
		try:
			dates[i["town"]].append(age(i["birth_date"], date))
		except:
			dates.update({i["town"]:age(i["birth_date"], date)})
	return dates

cpdef mypercentile(list array, list date):
	cdef datesss = datess(array, date)
	cdef k
	cdef i
	cdef result
	for i, k in datesss.items():
		result = {"town":i}
		result["p50"] = int(np.percentile(k, 50))
		result["p75"] = int(np.percentile(k, 75))
		result["p99"] = int(np.percentile(k, 99))
		datesss[i] = result
	return datesss



cpdef mybirthdays(list citizens):
	cdef dict content = {}
	cdef i
	cdef k
	cdef month
	cdef result
	cdef dict data = {"1":{}, "2":{}, "3":{}, "4":{}, "5":{}, "6":{}, "7":{}, "8":{}, "9":{}, "10":{}, "11":{}, "12":{}}
	for i in citizens:
		content.update({i["citizen_id"] : int(i["birth_date"].split(".")[1])})
	
	for i in citizens:
		for k in i["relatives"]:
			month = content[k]
			try:
				data[str(month)][i["citizen_id"]] += 1
			except:
				data[str(month)].update({i["citizen_id"] : 1})

	for m, i in data.items():
		result = []
		for k, n in i.items():
			result.append({"citizen_id":int(k), "presents":int(n)})
		data[m] = list(result)








cpdef recommit_data(dict new, list old, int citizen_id):
	cdef dict old_mass = {}
	cdef k
	cdef i

	for i in range(len(old)):
		old_mass.update({old[i]["citizen_id"] : [old[i], i]})


	cdef relatives = set(new["relatives"])
	cdef last_relatives = set(old_mass[citizen_id][0]["relatives"])
	cdef value_append = relatives - last_relatives
	cdef value_remove = last_relatives - relatives


	for i, k in new.items():
		old[old_mass[citizen_id][1]].update({i:k})


	for i in value_append:
		old[old_mass[i][1]]["relatives"].append(citizen_id)

	for i in value_remove:
		old[old_mass[i][1]]["relatives"].remove(citizen_id)

	return {"citizens":old}, {"data":old[old_mass[citizen_id][1]]}