import sys
import time
import os
import random
import mysql.connector
from mimesis import Person, Address
from mimesis.enums import Gender
from json import loads, dumps

# инициализация mysql-connector
try:
	cnx = mysql.connector.connect(user=os.environ.get("DATABASE_USER") or "root", password=os.environ.get("DATABASE_PASSWORD") or "mypassword", host="127.0.0.1", database="flasky")
	cursor = cnx.cursor()
except:
	print("Error: Not Connect to database!!!!")

# инициализация классов mimesis
person = Person("ru")
address = Address("ru")


def delete_from_tables():
	try:
		# удаление данных из тестовой таблицы
		cursor.execute("DROP TABLES persons, birthdays, percentiles, booleans;")
		cursor.execute("CREATE TABLE persons(id INT PRIMARY KEY auto_increment, value JSON not null) CHARACTER SET utf8 COLLATE utf8_general_ci;")
		cursor.execute("CREATE TABLE birthdays(id INT PRIMARY KEY auto_increment, value JSON not null);")
		cursor.execute("CREATE TABLE percentiles(id INT PRIMARY KEY auto_increment, value JSON not null, date datetime not null) CHARACTER SET utf8 COLLATE utf8_general_ci;")
		cursor.execute("CREATE TABLE booleans(id INT PRIMARY KEY auto_increment, birthday_bool  tinyint(1) not null, percentile_bool  tinyint(1) not null);")
		cnx.commit()
		# остановка соединения
		cursor.close()
		cnx.close()
	except:
		print("Error: can't remove data from table")


# эта функция генерирует информацию
# о людях, их колличество равно persons


# no valid code = 4, invalid geneder value
# no valid code = 3, invalid relatives
# no valid code = 2, invalid birth_date
# no valid code = 1, invalid table_places, example: apartment = 1, apartaament = 1 ...
def generate_person(persons, no_valid=False):
	data = {"citizens":[]}
	if no_valid:
		code = random.randint(1, 4)
	else:
		code = 0
	# структура {int citizen_id : list of relatives}
	# counter родственных связей
	value = 1000
	relatives = {1:[]}
	# заполняем ассоциативный массив родственников
	for i in range(2, int(persons)+1):
		result = []
		if code == 3:
			# добавим ненормальное значение
			relatives[1].append(int(persons) + 1000)
			# обнулим code
			code = 0
		for k in range(random.randint(1, value)):
			c = random.randint(1, i-1)
			if c not in result:
				result.append(c)
		for citizen in result:
			if i not in relatives[citizen]:
				relatives[citizen].append(i)
		relatives[i] = list(result)
	# генерируем остальную информацию
	for i in range(1, int(persons)+1):
		# пол муж/жен
		gender = ["male" if random.randint(0, 1) == 0 else "female"][0]

		# имя
		if gender == "male":
			name = person.full_name(Gender.MALE)
		else:
			name = person.full_name(Gender.FEMALE)

		# улица
		street = address.street_name()

		# город
		town = address.city()

		# строение
		building = str(random.randint(1, 134)) + "к" + str(random.randint(1, 23)) + "стр"

		# квартира
		apartment = random.randint(1, 146)

		#дату рождения
		birth_date = "{}.{}.{}".format(str(random.randint(1, 28)), 
										str(random.randint(1, 12)), 
										str(random.randint(1940, 2010)))
		if code == 2:
			birth_date = "{}.{}.{}".format(str(random.randint(32, 50)), str(random.randint(13, 15)), str(random.randint(1940, 2010)))
			code = 0

		# id
		citizen_id = int(i)

		# родственники (сборка из того что сделали)
		relatives_1 = relatives[i]

		if code == 4:
			gender = "sdfhowjehkj"
			# code использован, можно обнулить
			code = 0
		# добавляем в data всю информацию
		if code != 1:
			data["citizens"].append({"citizen_id":citizen_id, 
									"town":town, 
									"name":name, 
									"street":street, 
									"building":building, 
									"apartment":apartment, 
									"birth_date":birth_date, 
									"gender":gender, 
									"relatives":relatives_1})
		else:
			# невалидная информация
			data["citizens"].append({"citizen_id":citizen_id, 
							"todwnfs":town, 
							"nadmsde":name, 
							"strfdgeesdft":street, 
							"bufgilasfsding":building, 
							"apartaaaament":apartment, 
							"birth_dsadate":birth_date, 
							"gesdnder":gender, 
							"relaaatives":relatives_1})
			# обнуляем code
			code = 0
	return data


class Test:
	def __init__(self, app):
		self.app = app
		self.counter = 0
		
	# route 1
	def parse(self, arg, no_valid_code):
		# таймер
		start = time.time()

		try:
			# запросы
			status = self.app.post("/imports", data=dumps(self.mass), content_type='application/json').status_code
			# результат
			if status == no_valid_code:
				raise AttributeError("no valid code is {}, must be {}".format(status, no_valid_code))
			print("  1. [+]", "{} sec".format(time.time()-start), status)
			print("  -------------- OK ---------------", "\n")

			self.counter += 1
		except Exception as e:
			print("  1. [-] ERROR",  e)

	# route 2
	def reload(self, persons, no_valid_code):
		try:
			# генерируем новую информацию
			numbers = []
			numbers.append([1, 3, generate_person(1)["citizens"][0]])
			# засекаем время
			start = time.time()
			try:
				for i, k, c in numbers:
					# запросы
					status = self.app.patch("/imports/" + str(i) + "/citizens/" + str(k), data=dumps(c), content_type='application/json').status_code
			except:
				pass

			# результат
			print("  2. [+]",  "{} sec".format(time.time()-start), status)
			print("  -------------- OK ---------------", "\n")

			# счетчик
			self.counter += 1
			if status == 400 and status!=no_valid_code:
				delete_from_tables()
				sys.exit(1)

		# в случае ошибки
		except Exception as e:
			print("  2. [-] ERROR",  e)

	# route 3
	def citizens(self):
		try:
			# засекаем время
			start = time.time()
			# запрос
			status = self.app.get("/imports/1/citizens").status_code
			# результат
			print("  3. [+]",  "{} sec".format(time.time()-start), status)
			print("  -------------- OK ---------------", "\n")

			# счетчик
			self.counter += 1

		# в случае ошибки
		except Exception as e:
			print("  3. [-] ERROR",  e)

	# route 4
	def birthdays(self):
		try:
			# таймер
			start = time.time()
			# запрос
			status = self.app.get("/imports/1/citizens/birthdays").status_code
			# результат
			print("  4. [+]",  "{} sec".format(time.time()-start), status)
			print("  -------------- OK ---------------", "\n")

			# счетчик
			self.counter += 1

		# в случае ошибки
		except Exception as e:
			print("  4. [-] ERROR",  e)

	# route 5
	def percentile(self):
		try:
			# засекаем время
			start = time.time()
			# запрос
			status = self.app.get("/imports/1/towns/stat/percentile/age").status_code
			# результат
			print("  5. [+]",  "{} sec".format(time.time()-start), status_code)
			print("  -------------- OK ---------------", "\n")

			# счетчик
			self.counter += 1
		# в случае ошибки
		except Exception as e:
			print("  5. [-] ERROR",  e)

	# запускает тест
	def run_test(self, peoples):

		# генерируем людей
		if random.randint(1, 3) == 1:
			no_valid = True
			no_valid_code = 201
			print("  generated data is not valid\n")
		else:
			no_valid = False
			no_valid_code = 400
			print("  generated data is valid\n")

		self.mass = generate_person(peoples, no_valid)
		# вызываем все 5 функций
		self.parse(peoples, no_valid_code=no_valid_code)
		time.sleep(1)
		self.reload(peoples, no_valid_code=no_valid_code)
		time.sleep(1)
		self.citizens()
		time.sleep(1)
		self.birthdays()
		time.sleep(1)
		self.percentile()

		# очищаем таблицу
		delete_from_tables()

		print(" ===========", self.counter, "routers is OK ===========")
