import sys
#This path is for Connor's computer and it is working, when for some reason the normal ../ thing was literally just inserting "../" as a path.  Gotta get that fixed.
sys.path.append('..')

#print(sys.path)

import unittest
from source import dbconnect
from source import converters
import datetime

#This code is here temporarily .



class TestConverters(unittest.TestCase):

	def setUp(self):
		self.db = dbconnect.dbconnect()
		self.id1 = '10000000'
		self.fname1 = 'Joe'
		self.lname1 = 'Fire'
		self.id2 = '10000001'
		self.fname2 = 'James'
		self.lname2 = 'Smokes'
		self.id3 = '10000002'
		self.fname3 = 'Jane'
		self.lname3 = 'Inferno'
		
		self.db.i_query("INSERT INTO person (id, fname, lname) VALUES ('%s', '%s', '%s');" % (self.id1, self.fname1, self.lname1))
		self.db.i_query("INSERT INTO person (id, fname, lname) VALUES ('%s', '%s', '%s');" % (self.id2, self.fname2, self.lname2))
		self.db.i_query("INSERT INTO person (id, fname, lname) VALUES ('%s', '%s', '%s');" % (self.id3, self.fname3, self.lname3))
		
		self.filepath = r'C:\Users\crash\Documents\Field Session\Repo\CS-Fire-Team\UnitTestReport.xls'
	
	#def test_load_names():
	
	def test_convert_schedule(self):
		converters.convert_iar(self.filepath)
		
		shifts1 = self.db.get_shifts(self.id1, '2019-6-1', '2019-6-2')
		shifts2 = self.db.get_shifts(self.id2, '2019-6-1', '2019-6-2')
		shifts3 = self.db.get_shifts(self.id3, '2019-6-1', '2019-6-2')
		
		self.assertEqual(self.fname1, self.db.get_person_name(self.id1)[1])
		self.assertEqual(self.fname2, self.db.get_person_name(self.id2)[1])
		self.assertEqual(self.lname3, self.db.get_person_name(self.id3)[2])
		self.assertEqual(shifts2[0][1], datetime.datetime.strptime('2019-5-31 17:00:00', '%Y-%m-%d %H:%M:%S'))
		self.assertEqual(shifts1[0][1], datetime.datetime.strptime('2019-5-30 07:00:00', '%Y-%m-%d %H:%M:%S'))
		

	#def test_select(self):
    #    self.db.i_query("INSERT INTO person (id, fname, lname) VALUES ('%s', '%s', '%s');" % (self.id, self.fname, self.lname))
	#	results = self.db.s_query("SELECT fname FROM person WHERE id='%s';" % (self.id))
	#	self.assertEqual(self.fname, results[0][0])
    #    self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id))

	#def test_load_person(self):
    #   self.db.load_person(self.id, self.)

	#def test_individual_report(self):

    #           self.db.load_shift('05-11-2019 6:00 AM', '05-11-2019 12:00 PM', 1)
    #            self.db.load_shift('05-12-2019 6:00 AM', '05-12-2019 12:00 PM', 1)
    #            self.db.load_shift('05-13-2019 6:00 AM', '05-13-2019 12:00 PM', 1)
    #            self.db.load_shift('05-14-2019 6:00 AM', '05-14-2019 12:00 PM', 1)
    #            self.db.load_person_xref_shift('5-11-2019 6:00 AM', '5-11-2019 12:00 PM', '999999')
    #            self.db.load_person_xref_shift('5-12-2019 6:00 AM', '5-12-2019 12:00 PM', '999999')
    #            self.db.load_person_xref_shift('5-13-2019 6:00 AM', '5-13-2019 12:00 PM', '999999')
    #            self.db.load_person_xref_shift('5-14-2019 6:00 AM', '5-14-2019 12:00 PM', '999999')
    #            self.db.load_incident(10, '05-11-2019 7:56', 'Car Accident', '1 minute 30 seconds')
    #            self.db.load_incident(11, '05-11-2019 8:56', 'Car Accident', '1 minute 30 seconds')
    #            self.db.load_person_xref_incident('10', '999999', 'Station 1')
    #            self.db.load_person_xref_incident('11', '999999', 'Station 1')
    #            self.db.load_event('05-19-2019 10:00 AM', '05-19-2019 11:00 AM', 'Training')
    #            self.db.load_person_xref_event('05-19-2019 10:00 AM', '05-19-2019 11:00 AM', 'Training', '999999')
    #            self.db.load_event('05-18-2019 10:00 AM', '05-18-2019 11:00 AM', 'Fundraiser')
    #            self.db.load_person_xref_event('05-18-2019 10:00 AM', '05-18-2019 11:00 AM', 'Fundraiser', '999999')
    #            self.db.load_event('05-17-2019 10:00 AM', '05-17-2019 11:00 AM', 'Meeting')
    #            self.db.load_person_xref_event('05-17-2019 10:00 AM', '05-17-2019 11:00 AM', 'Meeting', '999999')
    #            self.db.load_event('05-16-2019 10:00 AM', '05-16-2019 11:00 AM', 'Apparatus')
    #            self.db.load_person_xref_event('05-16-2019 10:00 AM', '05-16-2019 11:00 AM', 'Apparatus', '999999')
    #            self.db.load_event('05-16-2019 11:00 AM', '05-16-2019 12:00 PM', 'Work Detail')
    #            self.db.load_person_xref_event('05-16-2019 11:00 AM', '05-16-2019 12:00 PM', 'Work Detail', '999999')

    #            report = self.generate_individual_report(self.id, self.startDate, self.endDate, 'Regular')
    #            self.assertEqual(4, report.shifts)
    #            self.assertEqual(2, report.actCalls)
    #            self.assertEqual(10, report.totCalls)
    #            self.assertEqual(3, report.WDHours)
    #            self.assertEqual(1, report.apparatus)
    #            self.assertEqual(1, report.fundraisers)
    #            self.assertEqual(1, report.meetings)
    #            self.assertEqual(1, report.trainings)
    #            self.assertEqual(1, report.totTrainings)
    #            
	def tearDown(self):
		self.db.i_query("DELETE FROM shift WHERE person_id='%s';" % (self.id1))
		self.db.i_query("DELETE FROM shift WHERE person_id='%s';" % (self.id2))
		self.db.i_query("DELETE FROM shift WHERE person_id='%s';" % (self.id3))
		self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id1))
		self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id2))
		self.db.i_query("DELETE FROM person WHERE id='%s';" % (self.id3))
		self.db.close()

if __name__ == '__man__':
	unittest.main()

#Python -m unittest filepath