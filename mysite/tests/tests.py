import sys
import time
import random
import mysql.connector
from mimesis import Person, Address
from mimesis.enums import Gender
from json import loads, dumps

# инициализация mysql-connector
try:
	cnx = mysql.connector.connect(user="root", password="mypassword", host="127.0.0.1", database="flasky")
	cursor = cnx.cursor()
except:
	print("Error: Not Connect to database!!!!")

# инициализация классов mimesis
person = Person("ru")
address = Address("ru")


# эта функция генерирует информацию
# о людях, их колличество равно persons
def generate_person(persons):
	data = {"citizens":[]}
	# структура {int citizen_id : list of relatives}
	relatives = {1:[]}
	# counter родственных связей
	value = int(persons/2)
	# заполняем ассоциативный массив родственников
	for i in range(2, int(persons)+1):
		result = []
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
		# id
		citizen_id = int(i)
		# родственники (сборка из того что есть)
		relatives_1 = relatives[i]

		# добавляем в data всю информацию
		data["citizens"].append({"citizen_id":citizen_id, 
								"town":town, 
								"name":name, 
								"street":street, 
								"building":building, 
								"apartment":apartment, 
								"birth_date":birth_date, 
								"gender":gender,
								"relatives":relatives_1})

	return data


class Test:
	def __init__(self, app):
		self.app = app
		self.counter = 0
		
	# route 1
	def parse(self, arg):
		# таймер
		start = time.time()
			# запрос
		status = self.app.post("/imports", data=dumps(self.mass), content_type='application/json').status_code
		# результат
		print("  1. [+]", "{}sec".format(time.time()-start), " HTTP POST", status)
		print("  -------------- OK ---------------", "\n")

		self.counter += 1
		# except Exception as e:
		# 	print("  1. [-] ERROR",  e)

	# route 2
	def reload(self, persons):
		try:
			# определяем колличество пользователей
			# у которых изменим поля
			if persons >= 10:
				counter = 10
			else:
				counter = int(persons)
			numbers = []
			# генерируем новую информацию
			for i in range(counter):
				number = random.randint(1, len(self.mass))
				numbers.append([[int(numder/2000) if int(number/2000)!=0 else 1][0], number%2000, generate_person(1)["citizens"][0]])
			# засекаем время
			start = time.time()
			status = 400
			for i, k, c in numbers:
				# запросы
				status = self.app.patch("/imports/" + str(i) + "/citizens/" + str(k), data=dumps(c), content_type='application/json').status_code

			# результат
			print("  2. [+]",  "{}sec".format((time.time()-start)/counter), " HTTP PATCH", status)
			print("  -------------- OK ---------------", "\n")

			# счетчик
			self.counter += 1

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
			print("  3. [+]",  "{}sec".format(time.time()-start), " HTTP GET", status)
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
			print("  4. [+]",  "{}sec".format(time.time()-start), " HTTP GET", status)
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
			print("  5. [+]",  "{}sec".format(time.time()-start), " HTTP GET", status)
			print("  -------------- OK ---------------", "\n")

			# счетчик
			self.counter += 1
		# в случае ошибки
		except Exception as e:
			print("  5. [-] ERROR",  e)

	# запускает тест
	def run_test(self, peoples):

		# генерируем людей
		self.mass = generate_person(peoples)

		# вызываем все 5 функций
		self.parse(peoples)
		time.sleep(1)
		self.reload(peoples)
		time.sleep(1)
		self.citizens()
		time.sleep(1)
		self.birthdays()
		time.sleep(1)
		self.percentile()

		# очищаем таблицу
		try:
			# удаление данных из тестовой таблицы
			cursor.execute("DELETE FROM flasky.persons;")
			cnx.commit()
			# остановка соединения
			cursor.close()
			cnx.close()
		except:
			print("Error: can't remove data from table")

		print(" ===========", self.counter, "routers is OK ===========")
