from dbconnect import dbconnect
import unittest

class TestDBConnect(unittest.TestCase):

	def test_select(self):
		db = dbconnect()
		db.connect()
		results = db.run_query("SELECT fname FROM person WHERE lname='Fire';")
		self.assertEqual('James', results[0][0])

	def test_insert(self):
		db = dbconnect()
		db.connect()
		db.run_query("INSERT INTO person (id, fname, lname) VALUES ('999999', 'Joji', 'Seshamekish');")
		results = db.run_query("SELECT id, fname, lname FROM person WHERE id='999999';")
		self.assertEqual('999999', results[0][0])
		self.assertEqual('Joji', results[1][0])
		self.assertEqual('Seshamekish', results[2][0])

	def test_update(self):
		

	if __name__ == '__man__':
		unittest.main()