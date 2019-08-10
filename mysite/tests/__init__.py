import sys
import logging
from .tests import Test
from .setting import log


class MyTest:
	def __init__(self, app):
		self.test = Test(app)
	def run(self):
		enters = 2
		try:
			peoples = sys.argv[2]
			print("\n", "========== Tests is started =========", "\n")
		except:
			print("You must be Enter the number of people, \nexample: 'python manage.py runtest 10000'" + "\n"*enters)
			print("--------- 0 tests is run ----------")
			return 0
		self.test.run_test(peoples=int(peoples))