
import psycopg2
from report import Report
import datetime

"""
    Args:
        query: string that represents the query to be run

    Returns:
        a tuple of lists where each entry in the tuple represents an entry in the table
        and each item in the list is a column
"""

class dbconnect():
    def connect(self):
        try:
            self.con = psycopg2.connect(
            dbname='bridge_db',
            user='csfire',
            port=5432,
            host='bridge-db.c6xgclrgfvud.us-west-1.rds.amazonaws.com',
            password='thebridge')
            self.cur = self.con.cursor()
        except psycopg2.Error:
            print('Failed to connect to DB')

    def s_query(self, query):
        try:
            self.connect()
            self.cur.execute(query)
            return self.cur.fetchall()
        except psycopg2.Error as e:
            print('Query error')
            print (e)

    def i_query(self, query):
        try:
            self.cur.execute(query)
            self.con.commit()
        except psycopg2.Error as e:
            print('Query error')
            print (e)

    def close(self):
        self.cur.close()
        self.con.close()

    def generate_for_all(self, startTime, endTime, reportType):
        numsQuery = "SELECT id FROM PERSON;"
        nums = self.s_query(numsQuery)
        reports = []
        for emp in nums:
            reports.append(self.generate_for_individual(emp, startTime, endTime, reportType))
        return reports

    def generate_for_some(self, empNums, startTime, endTime, reportType):
        reports = []
        for emp in empNums:
            reports.append(self.generate_for_individual(emp, startTime, endTime, reportType))
        return reports

    def generate_for_individual(self, empNum, startTime, endTime, reportType):
        empReport = Report(empNum, startTime, endTime)
        empReport.compute_full_report()
        return empReport
    
    #Loads a person.
    def load_person(person_id, note, time):
            d = dbconnect()
            d.i_query("INSERT INTO person (person_id, note, created_at) VALUES ('%s', '%s', '%s');" % (person_id, note, time))

    #Takes in incident id, time, category, and response.
    def load_incident(id, time, category, response):
            d = dbconnect()
            d.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES ('%s', '%s', '%s', '%s');" % (id, time, category, response))

    #Takes in an incident id and a list of personnel who responded and where they came from.
    def load_person_xref_incident(id, response):
            d = dbconnect()
            for r, s in response:
                    d.i_query("INSERT INTO person_xref_incident (incident_id, person_id, origin) VALUES ('%s', '%s', '%s');" % (id, r, s))

    #Loads a note if time is known
    def load_note(person_id, note, time):
            d = dbconnect()
            d.i_query("INSERT INTO note (person_id, note, created_at) VALUES ('%s', '%s', '%s');" % (person_id, note, time))

    #Loads a note if time is not known
    def load_note(person_id, note):
            d = dbconnect()
            d.i_query("INSERT INTO note (person_id, note) VALUES ('%s', '%s');" % (person_id, note))

    #Loads a shift.  
    def load_shift(tstart, tend, station):
            d = dbconnect()
            d.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('%s', '%s', '%s');" % (tstart, tend, station))

    #Loads a connection between a shift and a person.  "person" is a list of pairs or equivalent
    def load_person_xref_shift(shift_start, shift_end, person):
            d = dbconnect()
            for p, r in person:
                    d.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('%s', '%s', '%s', '%s');" % (p, shift_start, shift_end, r))
            
    #Loads a person_status change
    def load_person_status(status, date_change, person_id):
            d = dbconnect()
            d.i_query("INSERT INTO person_status (status, date_change, person_id) VALUES ('%s', '%s', '%s');" % (status, date_change, person_id))

    #Loads an event
    def load_event(tstart, tend, etype):
            d = dbconnect()
            d.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('%s', '%s', '%s');" % (tstart, tend, etype))

    #Loads a person_xref_event.  Person_id is a LIST of all the ids for the people who worked an event.	
    def load_person_xref_event(tstart, tend, etype, person_id):
            d = dbconnect()
            for p in people_id:
                    d.i_query("INSERT INTO person_xref_event (tstart, tend, etype, person_id) VALUES ('%s', '%s', '%s', '%s');" % (tstart, tend, etype, p))
