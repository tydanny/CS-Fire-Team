from dbconnect import dbconnect
from report import Report
import unittest

class TestDBConnect(unittest.TestCase):

	def setUp(self):
		self.db = dbconnect()
		self.id = '999999'
		self.fname = 'Joji'
		self.lname = 'Seshamekish'
		self.title = 'Fire Fighter'
		self.resident = 'Non-Resident'
		self.startDate = '2019-05-10'
		self.endDate = '2019-05-20'

	def test_insert(self):
		self.db.i_query("INSERT INTO person (id, fname, lname) VALUES ('%s', '%s', '%s');" % (self.id, self.fname, self.lname))
		results = self.db.s_query("SELECT id, fname, lname FROM person WHERE id='%s';" % (self.id))
		self.assertEqual(self.id, results[0][0])
		self.assertEqual(self.fname, results[0][1])
		self.assertEqual(self.lname, results[0][2])
        self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id))

	def test_select(self):
        self.db.i_query("INSERT INTO person (id, fname, lname) VALUES ('%s', '%s', '%s');" % (self.id, self.fname, self.lname))
		results = self.db.s_query("SELECT fname FROM person WHERE id='%s';" % (self.id))
		self.assertEqual(self.fname, results[0][0])
        self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id))

    def test_load_person(self):
        self.db.load_person(self.id, self.)

	def test_individual_report(self):

                self.db.load_shift('05-11-2019 6:00 AM', '05-11-2019 12:00 PM', 1)
                self.db.load_shift('05-12-2019 6:00 AM', '05-12-2019 12:00 PM', 1)
                self.db.load_shift('05-13-2019 6:00 AM', '05-13-2019 12:00 PM', 1)
                self.db.load_shift('05-14-2019 6:00 AM', '05-14-2019 12:00 PM', 1)
                self.db.load_person_xref_shift('5-11-2019 6:00 AM', '5-11-2019 12:00 PM', '999999')
                self.db.load_person_xref_shift('5-12-2019 6:00 AM', '5-12-2019 12:00 PM', '999999')
                self.db.load_person_xref_shift('5-13-2019 6:00 AM', '5-13-2019 12:00 PM', '999999')
                self.db.load_person_xref_shift('5-14-2019 6:00 AM', '5-14-2019 12:00 PM', '999999')
                self.db.load_incident(10, '05-11-2019 7:56', 'Car Accident', '1 minute 30 seconds')
                self.db.load_incident(11, '05-11-2019 8:56', 'Car Accident', '1 minute 30 seconds')
                self.db.load_person_xref_incident('10', '999999', 'Station 1')
                self.db.load_person_xref_incident('11', '999999', 'Station 1')
                self.db.load_event('05-19-2019 10:00 AM', '05-19-2019 11:00 AM', 'Training')
                self.db.load_person_xref_event('05-19-2019 10:00 AM', '05-19-2019 11:00 AM', 'Training', '999999')
                self.db.load_event('05-18-2019 10:00 AM', '05-18-2019 11:00 AM', 'Fundraiser')
                self.db.load_person_xref_event('05-18-2019 10:00 AM', '05-18-2019 11:00 AM', 'Fundraiser', '999999')
                self.db.load_event('05-17-2019 10:00 AM', '05-17-2019 11:00 AM', 'Meeting')
                self.db.load_person_xref_event('05-17-2019 10:00 AM', '05-17-2019 11:00 AM', 'Meeting', '999999')
                self.db.load_event('05-16-2019 10:00 AM', '05-16-2019 11:00 AM', 'Apparatus')
                self.db.load_person_xref_event('05-16-2019 10:00 AM', '05-16-2019 11:00 AM', 'Apparatus', '999999')
                self.db.load_event('05-16-2019 11:00 AM', '05-16-2019 12:00 PM', 'Work Detail')
                self.db.load_person_xref_event('05-16-2019 11:00 AM', '05-16-2019 12:00 PM', 'Work Detail', '999999')

                report = self.generate_individual_report(self.id, self.startDate, self.endDate, 'Regular')
                self.assertEqual(4, report.shifts)
                self.assertEqual(2, report.actCalls)
                self.assertEqual(10, report.totCalls)
                self.assertEqual(3, report.WDHours)
                self.assertEqual(1, report.apparatus)
                self.assertEqual(1, report.fundraisers)
                self.assertEqual(1, report.meetings)
                self.assertEqual(1, report.trainings)
                self.assertEqual(1, report.totTrainings)
                
	def tearDown(self):
		#self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id))
		self.db.close()

if __name__ == '__man__':
	unittest.main()
