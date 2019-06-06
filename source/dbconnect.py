import psycopg2

class dbconnect():
    def __init__(self):
        self.connect()
    def __del__(self):
        self.close()

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
            self.cur.execute(query)
            return self.cur.fetchall()
        except psycopg2.Error as e:
            print('Query error')
            print (e)

    def i_query(self, query):
        try:
            self.cur.execute(query)
            self.con.commit()
            print('yeet')
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
    def load_person(self, id, fname, lname, title, residency, start):
        self.i_query("INSERT INTO person (id, fname, lname, title, resident) VALUES ('%s', '%s', '%s', '%s', '%s');" % (id, fname, lname, title, residency))
        self.load_person_status('Active', start, id, 'Start Day')

    #Takes in incident id, time, category, and response.
    def load_incident(self, id, time, category, response):
        self.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES ('%s', '%s', '%s', '%s');" % (id, time, category, response))

    #Takes in an incident id and a list of personnel who responded and where they came from.
    def load_person_xref_incident(self, incident_id, person_id):
        for r, s in response:
            self.i_query("INSERT INTO person_xref_incident (incident_id, person_id) VALUES ('%s', '%s');" % (incident_id, person_id))

    #Loads a shift.  We should add in an if once we figure out the bonus column.
    def load_shift(self, shift_start, shift_end, station, person, role, bonus):
        self.i_query("INSERT INTO shift (person_id, shift_start, shift_end, station, role, bonus) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (person, shift_start, shift_end, station, role, bonus))
        
    #Loads a person_status change
    def load_person_status(self, status, date_change, person_id, note):
        self.i_query("INSERT INTO person_status (status, date_change, person_id, note) VALUES ('%s', '%s', '%s', '%s');" % (status, date_change, person_id, note))

    #Loads an event
    def load_event(self, id, tstart, tend, etype):
        self.i_query("INSERT INTO event (id, tstart, tend, etype) VALUES ('%s', '%s', '%s', '%s');" % (id, tstart, tend, etype))

    #Loads a person_xref_event.  Person_id is a LIST of all the ids for the people who worked an event.	
    def load_person_xref_event(self, event_id, person_id):
        for p in people_id:
            self.i_query("INSERT INTO person_xref_event (event_id, person_id) VALUES ('%s', '%s');" % (event_id, person_id))

    def get_person(self, id):
        return self.s_query("""
        SELECT * FROM person WHERE id='%s';
        """ % (id))

    def get_ids(self):
        return self.s_query("SELECT id FROM person")

    def get_statuses(self, id):
        return self.s_query("""
        SELECT * FROM person_status WHERE person_id='%s' ORDER BY date_change;
        """ % (id))

    def get_status_changes_for_range(self, id, start, end):
        return self.s_query("""
        SELECT * FROM person_status WHERE person_id='%s' AND date_change BETWEEN '%s' AND '%s' ORDER BY date_change;
        """ % (id, start, end))

    def get_events(self, id, start, end, type):
        return self.s_query("""
        SELECT * FROM person_xref_event WHERE person_id='%s' AND tstart BETWEEN '%s' AND '%s' AND type LIKE '%s';
        """ % (id, start, end, type))

    def get_start(self, id):
        return self.get_statuses(id)[0][1]

    def get_shifts(self, id, start, end):
        return self.s_query("""
        SELECT * FROM shift WHERE person_id='%s' AND shift_start BETWEEN '%s' and '%s';
        """ % (id, start, end))

    def get_shift(self, person_id, start, end):
        return self.s_query("""
        SELECT * FROM shift WHERE tstart='%s' AND tend='%s' AND person_id='%s';
        """ % (start, end, person_id))

    def get_actual_calls(self, id, start, end):
        return self.s_query("""
        SELECT * FROM incident WHERE tstamp BETWEEN '%s' AND '%s' AND id IN (SELECT incident_id FROM person_xref_incident WHERE person_id='%s');
        """ % (start, end, id))

    def get_num_actual_calls(self, id, start, end):
        return self.s_query("""
        SELECT COUNT(*) FROM incident AS i, person_xref_incident AS pi
        WHERE pi.person_id = '%s' AND i.id = pi.incident_id AND i.tstamp 
        BETWEEN '%s' AND '%s';""" % (id, start, end))

    def get_title(self, id):
        title = self.s_query("""
        SELECT title FROM person WHERE id='%s';
        """ % (id))
        return title[0][0]

    def update_permissions(self, id, newper):
        self.i_query("""
        UPDATE person SET title='%s' WHERE id='%s';
        """ % (newper, id))

    def delete_status(self, id, date_change, status):
        self.i_query("""
        DELETE FROM person_status WHERE person_id='%s' AND date_change='%s' AND status='%s';
        """ % (id, date_change, status))

    def get_wdt(self, id, start, end):
        return self.s_query("""
        SELECT e.tstart-e.tend FROM event AS e, person_xref_event AS pe WHERE e.id = pe.event_id AND pe.person_id = '%s'
        AND e.tstart BETWEEN '%s' AND '%s' AND e.etype LIKE 'WORK DETAIL%%';
        """ % (id, start, end))

    #Gets all shifts for one person in a range.
    def get_shift_duration(self, id, start, end):
        return self.s_query("""
        SELECT shift_end-shift_start, shift_start, shift_end FROM shift 
        WHERE person_id = '%s' AND shift_start BETWEEN '%s' AND '%s';
        """ % (id, start, end))

    def get_appar(self, id, start, end):
        return self.s_query("""
        SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.id = pe.event_id
        AND (e.etype = 'work detail-daily' OR e.etype = 'work detail-weekly' OR e.etype = '
        work detail-sunday');""" % (id, start, end))

    def get_fundraisers(self, id, start, end):
        return self.s_query("""
        SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.id = pe.event_id
        AND (e.etype = 'work detail-daily' OR e.etype = 'work detail-weekly' OR e.etype = '
        work detail-sunday');""" % (id, start, end))

    def get_meetings(self, id, start, end):
        return self.s_query("""
        SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.id = pe.event_id
        AND e.etype = 'meeting';""" % (id, start, end))

    def get_trainings(self, id, start, end):
        return self.s_query("""
        SELECT e.tend-e.tstart, e.etype FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.etype LIKE 'training%%' AND e.tstart BETWEEN '%s'
        AND '%s' AND e.id = pe.event_id;""" % (id, start, end))
