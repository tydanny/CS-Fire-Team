from dbconnect import dbconnect
from report import Report
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
        self.db.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('05-11-2019 6:00 AM', '05-11-2019 12:00 PM', 1, 'Fire Fighter');")
        self.db.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end) VALUES ('999999', '5-11-2019 6:00 AM', '5-11-2019 12:00 PM');")
        self.db.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end) VALUES ('999999', '5-12-2019 6:00 AM', '5-12-2019 12:00 PM');")
        self.db.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end) VALUES ('999999', '5-13-2019 6:00 AM', '5-13-2019 12:00 PM');")
        self.db.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end) VALUES ('999999', '5-14-2019 6:00 AM', '5-14-2019 12:00 PM');")
        self.db.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES (10, '05-11-2019 7:56', 'Car Accident', '1 minute 30 seconds');")
        self.db.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES (11, '05-11-2019 8:56', 'Car Accident', '1 minute 30 seconds');")
        self.db.i_query("INSERT INTO person_xref_incident (person_id, incident_id, origin) VALUES ('999999', '10', 'Station 1');")
        self.db.i_query("INSERT INTO person_xref_incident (person_id, incident_id, origin) VALUES ('999999', '11', 'Station 1');")
        self.db.i_query("INSERT INTO event (tstart, tend, type) VALUES ('05-19-2019 10:00 AM', '05-19-2019 11:00 AM', 'Training');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('05-19-2019 10:00 AM', '05-19-2019 11:00 AM', 'Training', '999999');")
        self.db.i_query("INSERT INTO event (tstart, tend, type) VALUES ('05-18-2019 10:00 AM', '05-18-2019 11:00 AM', 'Fundraiser');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('05-18-2019 10:00 AM', '05-18-2019 11:00 AM', 'Fundraiser', '999999');")
        self.db.i_query("INSERT INTO event (tstart, tend, type) VALUES ('05-17-2019 10:00 AM', '05-17-2019 11:00 AM', 'Meeting');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('05-17-2019 10:00 AM', '05-17-2019 11:00 AM', 'Meeting', '999999');")
        self.db.i_query("INSERT INTO event (tstart, tend, type) VALUES ('05-16-2019 10:00 AM', '05-16-2019 11:00 AM', 'Apparatus');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('05-16-2019 10:00 AM', '05-16-2019 11:00 AM', 'Apparatus', '999999');")
        self.db.i_query("INSERT INTO event (tstart, tend, type) VALUES ('05-16-2019 11:00 AM', '05-16-2019 12:00 PM', 'Work Detail');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('05-16-2019 11:00 AM', '05-16-2019 12:00 PM', 'Work Detail', '999999');")

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
