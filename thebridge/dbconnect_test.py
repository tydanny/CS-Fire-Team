from dbconnect import dbconnect
import unittest

class TestDBConnect(unittest.TestCase):

	def setUp(self):
		self.db = dbconnect()
		self.db.connect()
		self.id = '999999'
		self.fname = 'Joji'
		self.lname = 'Seshamekish'
		self.title = 'Fire Fighter'
		self.resident = 'Non-Resident'

	def test_insert(self):
		self.db.i_query("INSERT INTO person (id, fname, lname) VALUES ('%s', '%s', '%s');" % (self.id, self.fname, self.lname))
		results = self.db.s_query("SELECT id, fname, lname FROM person WHERE id='%s';" % (self.id))
		self.assertEqual(self.id, results[0][0])
		self.assertEqual(self.fname, results[0][1])
		self.assertEqual(self.lname, results[0][2])

	def test_select(self):
		results = self.db.s_query("SELECT fname FROM person WHERE id='%s';" % (self.id))
		self.assertEqual(self.fname, results[0][0])

	def test_update(self):
		self.db.i_query("UPDATE person SET title='%s', resident='%s' WHERE id='%s';" % (self.title, self.resident, self.id))
		results = self.db.s_query("SELECT title, resident FROM person WHERE id='%s';" % (self.id))
		self.assertEqual(self.title, results[0][0])
		self.assertEqual(self.resident, results[0][1])
		self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id))

	def tearDown(self):
		#self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id))
		self.db.close()

if __name__ == '__man__':
	unittest.main()