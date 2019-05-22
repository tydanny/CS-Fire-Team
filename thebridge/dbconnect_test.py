from dbconnect import dbconnect
import unittest

class TestDBConnect(unittest.TestCase):

	def setUp(self):
		self.db = dbconnect()
		self.db.connect()

	def test_insert(self):
		self.db.run_query("INSERT INTO person (id, fname, lname) VALUES ('999999', 'Joji', 'Seshamekish');")
		results = self.db.run_query("SELECT id, fname, lname FROM person WHERE id='999999';")
		self.assertEqual('999999', results[0][0])
		self.assertEqual('Joji', results[1][0])
		self.assertEqual('Seshamekish', results[2][0])

	def test_select(self):
		results = self.db.run_query("SELECT fname FROM person WHERE id='999999';")
		self.assertEqual('Joji', results[0][0])

	def test_update(self):
		self.db.run_query("UPDATE person SET title='Fire Fighter', resident='Non-Resident' WHERE id='999999';")
		results = self.db.run_query("SELECT title, resident FROM person WHERE id='999999';")
		self.assertEqual('Fire Fighter', results[0][0])
		self.assertEqual('Non-Resident', results[1][0])

	def tearDown(self):
		self.db.run_query("DELETE FROM person WHERE id='999999';")

	if __name__ == '__man__':
		unittest.main()