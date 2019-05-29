
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
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.con = psycopg2.connect(
            dbname='dn73j2q782lcl',
            user='bhmqlaubbvqtsk',
            port=5432,
            host='ec2-50-19-114-27.compute-1.amazonaws.com',
            password='6a143a2104611cd12094839ee7853ed7c7ca2d3db74b2fff9d07e978fd8f941b')
            self.cur = self.con.cursor()
        except psycopg2.Error:
            print('Failed to connect to DB')

    def s_query(self, query):
        try:
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
    
    def generate_for_dept(self, startTime, endTime):
        
        actCalls = 0
        totCalls = 0
        WDHours = 0
        apparatus = 0
        fundraisers = 0
        meetings = 0
        trainings = 0
        totTrainings = 0
        
        numsQuery = "SELECT id FROM PERSON;"
        nums = self.s_query(numsQuery)
        
        for n in nums:
            rep = generate_for_individual(n, startTime, endTime)
            totCalls += rep.actCalls
            WDHours += rep.WDHours
            trainings += rep.trainings
            totTrainings += rep.totTrainings
            
        actCalls = self.s_query("SELECT COUNT(*) FROM incident;")
        apparatus = self.s_query("SELECT COUNT(*) FROM event WHERE etype = 'work detail-daily' OR etype = 'work detail-weekly' OR etype = 'work detail-sunday' AND tstart BETWEEN '%s' AND '%s';" % (startTime, endTime))
        fundraisers = self.s_query("SELECT COUNT(*) FROM event WHERE etype = 'work detail-fundraiser' AND tstart BETWEEN '%s' AND '%s';" % (startTime, endTime))
        meetings =  self.s_query("SELECT COUNT(*) FROM event WHERE etype = 'meeting' AND tstart BETWEEN '%s' AND '%s';" % (startTime, endTime))
        
    
    def generate_for_all(self, startTime, endTime, reportType):
        numsQuery = "SELECT id FROM PERSON;"
        nums = self.s_query(numsQuery)
        return self.generate_for_some(nums, startTime, endTime)

    def generate_for_some(self, empNums, startTime, endTime, reportType):
        reports = []
        for emp in empNums:
            reports.append(self.generate_for_individual(emp, startTime, endTime))
        return reports

    def generate_for_individual(self, empNum, startTime, endTime, reportType):
        report = Report(empNum, startTime, endTime)
        report.generate_full_report()
        return report

    #Loads a person.
    def load_person(self, person_id, fname, lname, title, residency, start):
        self.i_query("INSERT INTO person (id, fname, lname, title, resident) VALUES ('%s', '%s', '%s', '%s', '%s');" % (self.id, self.fname, self.lname))

    #Takes in incident id, time, category, and response.
    def load_incident(self, id, time, category, response):
        self.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES ('%s', '%s', '%s', '%s');" % (id, time, category, response))

    #Takes in an incident id and a list of personnel who responded and where they came from.
    def load_person_xref_incident(self, incident_id, person_id):
        for r, s in response:
            self.i_query("INSERT INTO person_xref_incident (incident_id, person_id) VALUES ('%s', '%s');" % (incident_id, person_id))

    #Loads a note if time is known
    def load_note(self, person_id, note, time):
        self.i_query("INSERT INTO note (person_id, note, created_at) VALUES ('%s', '%s', '%s');" % (person_id, note, time))

    #Loads a note if time is not known
    def load_note(self, person_id, note):
        self.i_query("INSERT INTO note (person_id, note) VALUES ('%s', '%s');" % (person_id, note))

    #Loads a shift.  
    def load_shift(self, tstart, tend, station):
        self.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('%s', '%s', '%s');" % (tstart, tend, station))

    #Loads a connection between a shift and a person.  THIS LIKELY NEEDS MODIFICATION BECAUSE WE KEEP CHANGING THE TABLES.
    def load_person_xref_shift(self, shift_start, shift_end, station, person, role):
        self.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role, station) VALUES ('%s', '%s', '%s', '%s', '%s');" % (person, shift_start, shift_end, role, station))
        
    #Loads a person_status change
    def load_person_status(self, status, date_change, person_id):
        self.i_query("INSERT INTO person_status (status, date_change, person_id) VALUES ('%s', '%s', '%s');" % (status, date_change, person_id))

    #Loads an event
    def load_event(self, tstart, tend, etype):
        self.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('%s', '%s', '%s');" % (tstart, tend, etype))

    #Loads a person_xref_event.  Person_id is a LIST of all the ids for the people who worked an event.	
    def load_person_xref_event(self, tstart, tend, etype, person_id):
        for p in people_id:
            self.i_query("INSERT INTO person_xref_event (tstart, tend, etype, person_id) VALUES ('%s', '%s', '%s', '%s');" % (tstart, tend, etype, p))

    def get_person(self, id1):
        return self.s_query("""
        SELECT * FROM person WHERE id='%s';
        """ % (id1))

    def get_person_from_name(self, fname, lname):
        return self.s_query("""
        SELECT id FROM person WHERE fname = '%s' AND lname = '%s';
        """ % (fname, lname))
    
    #May need modding because we keep changing shift.
    def get_shift(self, tstart, tend, location):
        return self.s_query("""
        SELECT * FROM shift WHERE tstart = '%s' AND tend = '%s' AND station = '%s';
        """ % (tstart, tend, location))

    def get_person_xref_shift(person, shift_start, shift_end, station):
      return self.s_query("""
        SELECT person_id, shift_start, station FROM person_xref_shift WHERE person_id = '%s' AND shift_start = '%s' AND shift_end = '%s' AND station = '%s';
        """ % (person, tstart, tend, location))
        
