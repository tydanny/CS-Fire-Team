
import psycopg2
from report import Report

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
        print("Reached generate for all")

    def generate_for_some(self, empNums, startTime, endTime, reportType):
        print("Reached generate for all")

    def generate_for_individual(self, empNum, startTime, endTime, reportType):
        print("Reached generate for individual")
        #This is not done
        s_query("" % (person_id, note, time))

    #Loads a person.
    def load_person(self, person_id, fname, lname, title, residency, start):
        self.i_query("INSERT INTO person (id, fname, lname, title, resident) VALUES ('%s', '%s', '%s', '%s', '%s');" % (self.id, self.fname, self.lname))
        self.close()

    #Takes in incident id, time, category, and response.
    def load_incident(self, id, time, category, response):
        self.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES ('%s', '%s', '%s', '%s');" % (id, time, category, response))
        self.close()

    #Takes in an incident id and a list of personnel who responded and where they came from.
    def load_person_xref_incident(self, id, response):
        for r, s in response:
            self.i_query("INSERT INTO person_xref_incident (incident_id, person_id, origin) VALUES ('%s', '%s', '%s');" % (id, r, s))
        self.close()

    #Loads a note if time is known
    def load_note(self, person_id, note, time):
        self.i_query("INSERT INTO note (person_id, note, created_at) VALUES ('%s', '%s', '%s');" % (person_id, note, time)))
        self.close()

    #Loads a note if time is not known
    def load_note(self, person_id, note):
        self.i_query("INSERT INTO note (person_id, note) VALUES ('%s', '%s');" % (person_id, note))
        self.close()

    #Loads a shift.  
    def load_shift(self, tstart, tend, station):
        self.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('%s', '%s', '%s');" % (tstart, tend, station))
        self.close()

    #Loads a connection between a shift and a person.  "person" is a list of pairs or equivalent
    def load_person_xref_shift(self, shift_start, shift_end, person):
        for p, r in person:
            self.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('%s', '%s', '%s', '%s');" % (p, shift_start, shift_end, r))
        self.close()
        
    #Loads a person_status change
    def load_person_status(self, status, date_change, person_id):
        self.i_query("INSERT INTO person_status (status, date_change, person_id) VALUES ('%s', '%s', '%s');" % (status, date_change, person_id))
        self.close()

    #Loads an event
    def load_event(self, tstart, tend, etype):
        self.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('%s', '%s', '%s');" % (tstart, tend, etype))
        self.close()

    #Loads a person_xref_event.  Person_id is a LIST of all the ids for the people who worked an event.	
    def load_person_xref_event(self, tstart, tend, etype, person_id):
        for p in people_id:
            self.i_query("INSERT INTO person_xref_event (tstart, tend, etype, person_id) VALUES ('%s', '%s', '%s', '%s');" % (tstart, tend, etype, p))
        self.close()

    def get_person(self, id):
        self.i_query("""
        SELECT * FROM person WHERE id='%s';
        """ % (id))