#firefighter_test.py
import unittest
from firefighter import Firefighter
from dbconnect import dbconnect

class TestFirefighter(unittest.TestCase):

    def setUp(self):
        self.db = dbconnect()
        self.db.connect()
        
        #create firefighter
        self.ff = Firefighter("Jane", "Doe", "246", "Firefighter", "Resident")

        #Insert information into tables
        #Create resident firefighter
        self.db.i_query("INSERT INTO person (id, fname, lname, title, resident) VALUES ('246', 'Jane', 'Doe', 'Firefighter', 'Resident');")
        
        #25 hours of training
        self.db.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('2019-01-02 08:00:00', '2019-01-02 11:00:00', 'Training');")
        self.db.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('2019-02-05 08:00:00', '2019-02-05 19:00:00', 'Training');")
        self.db.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('2019-03-08 07:00:00', '2019-03-08 18:00:00', 'Training');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('2019-01-02 08:00:00', '2019-01-02 11:00:00', 'Training', '246');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('2019-02-05 08:00:00', '2019-02-05 19:00:00', 'Training', '246');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('2019-03-08 07:00:00', '2019-03-08 18:00:00', 'Training', '246');")
        
        #4 Shifts
        self.db.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('2019-01-04 06:00:00', '2019-01-04 12:00:00', 1);")
        self.db.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('2019-01-05 06:00:00', '2019-01-05 12:00:00', 1);")
        self.db.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('2019-01-06 06:00:00', '2019-01-06 12:00:00', 1);")
        self.db.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('2019-01-07 06:00:00', '2019-01-07 12:00:00', 1);")
        self.db.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('246', '2019-01-04 06:00:00', '2019-01-04 12:00:00', 'Firefighter');")
        self.db.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('246', '2019-01-05 06:00:00', '2019-01-05 12:00:00', 'Firefighter');")
        self.db.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('246', '2019-01-06 06:00:00', '2019-01-06 12:00:00', 'Firefighter');")
        self.db.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('246', '2019-01-07 06:00:00', '2019-01-07 12:00:00', 'Firefighter');")

        #2 Actual Calls
        self.db.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES (13, '2019-02-19 17:56', 'Car Accident', '2 minutes 53 seconds');")
        self.db.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES (31, '2019-02-22 17:18', 'Car Accident', '8 minutes 12 seconds');")
        self.db.i_query("INSERT INTO person_xref_incident(person_id, incident_id) VALUES ('246', 13);")
        self.db.i_query("INSERT INTO person_xref_incident(person_id, incident_id) VALUES ('246', 31);")

        #13 Work Details (Includes time from fundraiser, sundays/weeklies, work detail, and meetings)
        self.db.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('2019-05-10 07:00:00', '2019-05-10 14:00:00', 'Work Detail');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('2019-05-10 07:00:00', '2019-05-10 14:00:00', 'Work Detail', '246');")


        #3 Apparatus (Weeklys and Sundays)
        self.db.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('2019-02-02 08:00:00', '2019-02-02 09:00:00', 'Weekly');")
        self.db.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('2019-05-05 08:00:00', '2019-05-05 09:00:00', 'Sunday');")
        self.db.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('2019-05-08 07:00:00', '2019-05-08 08:00:00', 'Weekly');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('2019-02-02 08:00:00', '2019-02-02 09:00:00', 'Weekly', '246');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('2019-05-05 08:00:00', '2019-05-05 09:00:00', 'Sunday', '246');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('2019-05-08 07:00:00', '2019-05-08 08:00:00', 'Weekly', '246');")      

        #1 Meeting
        self.db.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('2019-04-08 08:00:00', '2019-04-08 11:00:00', 'Meeting');")
        self.db.i_query("INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('2019-04-08 08:00:00', '2019-04-08 11:00:00', 'Meeting', '246');")

    def testSetTraining(self):
        self.ff.setTraining()
        self.assertEqual('25', self.ff.trainingHours)

    def testSetShifts(self):
        self.ff.setShifts()
        self.assertEqual('4', self.ff.shifts)

    def testSetCalls(self):
        self.ff.setActCalls()
        self.assertEqual('2', self.ff.actualCalls)

    def testSetWorkDetail(self):
        self.ff.setWorkDetail()
        self.assertEqual('13', self.ff.workDetail)

    def testSetApparatusChecks(self):
        self.ff.setApparatusChecks()
        self.assertEqual('3', self.ff.apparatusChecks)

    def testSetFundraisers(self):
        self.ff.setFundraisers()
        self.assertEqual('0', self.ff.fundraisers)

    def testSetMeetings(self):
        self.ff.setMeetings()
        self.assertEqual('1', self.ff.meetings)

    def tearDown(self):

        self.db.i_query("DELETE FROM event WHERE tstart = '2019-01-02 08:00:00' AND tend = '2019-01-02 11:00:00';")
        self.db.i_query("DELETE FROM event WHERE tstart = '2019-02-05 08:00:00' AND tend = '2019-02-05 19:00:00';")
        self.db.i_query("DELETE FROM event WHERE tstart = '2019-03-08 07:00:00' AND tend = '2019-03-08 18:00:00';")
        self.db.i_query("DELETE FROM person_xref_event WHERE tstart = '2019-01-02 08:00:00' AND tend = '2019-01-02 11:00:00' AND type = 'Training';")
        self.db.i_query("DELETE FROM person_xref_event WHERE tstart = '2019-02-05 08:00:00' AND tend = '2019-02-05 19:00:00' AND type = 'Training';")
        self.db.i_query("DELETE FROM person_xref_event WHERE tstart = '2019-03-08 07:00:00' AND tend = '2019-03-08 18:00:00' AND type = 'Training';")

        self.db.i_query("DELETE FROM shift WHERE tstart = '2019-01-04 06:00:00' AND tend = '2019-01-04 12:00:00';")
        self.db.i_query("DELETE FROM shift WHERE tstart = '2019-01-05 06:00:00' AND tend = '2019-01-05 12:00:00';")
        self.db.i_query("DELETE FROM shift WHERE tstart = '2019-01-06 06:00:00' AND tend = '2019-01-06 12:00:00';")
        self.db.i_query("DELETE FROM shift WHERE tstart = '2019-01-07 06:00:00' AND tend = '2019-01-07 12:00:00';")
        self.db.i_query("DELETE FROM person_xref_shift WHERE person_id = '246' AND shift_start = '2019-01-04 06:00:00' AND shift_end = '2019-01-04 12:00:00';")
        self.db.i_query("DELETE FROM person_xref_shift WHERE person_id = '246' AND shift_start = '2019-01-05 06:00:00' AND shift_end = '2019-01-05 12:00:00';")
        self.db.i_query("DELETE FROM person_xref_shift WHERE person_id = '246' AND shift_start = '2019-01-06 06:00:00' AND shift_end = '2019-01-06 12:00:00';")
        self.db.i_query("DELETE FROM person_xref_shift WHERE person_id = '246' AND shift_start = '2019-01-07 06:00:00' AND shift_end = '2019-01-07 12:00:00';")

        self.db.i_query("DELETE FROM incident WHERE id = 13;")
        self.db.i_query("DELETE FROM incident WHERE id = 31;")
        self.db.i_query("DELETE FROM person_xref_incident WHERE person_id = '246' AND incident_id = 13;")
        self.db.i_query("DELETE FROM person_xref_incident WHERE person_id = '246' AND incident_id = 31;")

        self.db.i_query("DELETE FROM event WHERE tstart = '2019-05-10 07:00:00' AND tend = '2019-05-10 14:00:00';")
        self.db.i_query("DELETE FROM person_xref_event WHERE tstart = '2019-05-10 07:00:00' AND tend = '2019-05-10 14:00:00' AND type = 'Work Detail';")

        self.db.i_query("DELETE FROM event WHERE tstart = '2019-02-02 08:00:00' AND tend = '2019-02-02 09:00:00';")
        self.db.i_query("DELETE FROM event WHERE tstart = '2019-05-05 08:00:00' AND tend = '2019-05-05 09:00:00';")
        self.db.i_query("DELETE FROM event WHERE tstart = '2019-05-08 07:00:00' AND tend = '2019-05-08 08:00:00';")
        self.db.i_query("DELETE FROM person_xref_event WHERE tstart = '2019-02-02 08:00:00' AND tend = '2019-02-02 09:00:00' AND type = 'Weekly';")
        self.db.i_query("DELETE FROM person_xref_event WHERE tstart = '2019-05-05 08:00:00' AND tend = '2019-05-05 09:00:00' AND type = 'Sunday';")
        self.db.i_query("DELETE FROM person_xref_event WHERE tstart = '2019-05-08 07:00:00' AND tend = '2019-05-08 08:00:00' AND type = 'Weekly';")

        self.db.i_query("DELETE FROM event WHERE tstart = '2019-04-08 08:00:00' AND tend = '2019-04-08 11:00:00';")
        self.db.i_query("DELETE FROM person_xref_event WHERE tstart = '2019-04-08 08:00:00' AND tend = '2019-04-08 11:00:00' AND type = 'Meeting';")

        self.db.i_query("DELETE FROM person WHERE id='246';")

    if __name__ == '__main__':
        unittest.main()
