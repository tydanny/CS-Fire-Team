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
            self.close()
            self.connect()

    def i_query(self, query):
        try:
            self.cur.execute(query)
            self.con.commit()
            print('yeet')
        except psycopg2.Error as e:
            print('Query error')
            print (e)
            self.close()
            self.connect()

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
        self.i_query("INSERT INTO person_xref_incident (incident_id, person_id) VALUES ('%s', '%s');" % (incident_id, person_id))

    #Loads a shift.  We should add in an if once we figure out the bonus column.
    def load_shift(self, shift_start, shift_end, station, person, bonus):
        self.i_query("INSERT INTO shift (person_id, shift_start, shift_end, station, bonus) VALUES ('%s', '%s', '%s', '%s', '%s');" % (person, shift_start, shift_end, station, bonus))
        
    #Loads a person_status change
    def load_person_status(self, status, date_change, person_id, note):
        self.i_query("INSERT INTO person_status (status, date_change, person_id, note) VALUES ('%s', '%s', '%s', '%s');" % (status, date_change, person_id, note))

    #Loads an event
    def load_event(self, id, tstart, etype):
        self.i_query("INSERT INTO event (id, tstart, etype) VALUES ('%s', '%s', '%s');" % (id, tstart, etype))

    #Loads a person_xref_event.  Person_id is a LIST of all the ids for the people who worked an event.	
    def load_person_xref_event(self, event_id, person_id, duration):
        self.i_query("INSERT INTO person_xref_event (event_id, person_id, duration) VALUES ('%s', '%s', %s);" % (event_id, person_id, duration))

    def load_class(self, id, tstart, duration, type):
        self.i_query("INSERT INTO class (id, tstart, duration, type) VALUES ('%s', '%s', '%s', '%s');" % (id, tstart, duration, type))

    def load_person_xref_class(self, class_id, person_id):
        self.i_query("INSERT INTO person_xref_class (class_id, person_id) VALUES ('%s', '%s');" % (class_id, person_id))

    def get_person(self, id):
        return self.s_query("""
        SELECT * FROM person WHERE id='%s';
        """ % (id))

    def get_person_name(self, id):
        fName = self.s_query("SELECT fname FROM person WHERE id = '%s'" % (id))[0][0]
        lName = self.s_query("SELECT lname FROM person WHERE id = '%s'" % (id))[0][0]
        return [id, fName, lName]

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
        SELECT * FROM event WHERE tstart BETWEEN '%s' AND '%s' AND id IN (SELECT event_id FROM person_xref_event
        WHERE person_id = '%s') AND etype LIKE '%s';
        """ % (start, end, id, type))

    def get_classes(self, id, start, type):
        return self.s_query("""
        SELECT * FROM class WHERE tstart BETWEEN '%s' AND '%s' AND id IN (SELECT class_id FROM person_xref_class
        WHERE person_id = '%s') AND etype LIKE '%s';
        """ % (start, end, id, type))

    def get_people(self):
        people = []
        people.append(self.s_query("SELECT id, fname, lname FROM person"))
        return people

    def get_active_people(self):
        stats = self.s_query("SELECT status, person_id FROM person_status WHERE date_change IN (SELECT MAX(date_change) FROM person_status group by person_id)")
        statuses = []
        people = []
        for s in stats:
            if s[0] != 'Resigned' and s[0] != 'Retired':
                statuses.append(s[1])
        
        for s in statuses:
            people.append(self.get_person_name(s))
        return people
   
    def get_start(self, id):
        return self.get_statuses(id)[0][1]

    def get_shifts(self, id, start, end):
        return self.s_query("""
        SELECT * FROM shift WHERE person_id='%s' AND shift_end BETWEEN '%s' and '%s';
        """ % (id, start, end))

    def get_shift(self, person_id, start, end):
        return self.s_query("""
        SELECT * FROM shift WHERE shift_start='%s' AND shift_end='%s' AND person_id='%s';
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

    def get_person_id(self, id):
        return self.s_query("""
        SELECT id FROM person WHERE id='%s';
        """ % (id))[0][0]

    def get_person_id_check(self, id):
        return self.s_query("""
        SELECT id FROM person WHERE id='%s';
        """ % (id))

    def get_title(self, id):
        title = self.s_query("""
        SELECT title FROM person WHERE id='%s';
        """ % (id))
        return title[0][0]
    
    def update_bonus(self, tstart, tend, person, bonus):
        self.i_query("""
        UPDATE shift SET bonus='%s' WHERE shift_start='%s' AND shift_end='%s' AND person_id='%s';
        """ % (newper, id))

    def update_permissions(self, id, newper):
        self.i_query("""
        UPDATE person SET title='%s' WHERE id='%s';
        """ % (bonus, tstart, tend, person))

    def delete_status(self, id, date_change, status):
        self.i_query("""
        DELETE FROM person_status WHERE person_id='%s' AND date_change='%s' AND status='%s';
        """ % (id, date_change, status))

    def get_wdt(self, id, start, end):
        return self.s_query("""
        SELECT duration FROM person_xref_event WHERE person_id='%s' AND event_id IN 
        (SELECT id FROM event WHERE (etype LIKE 'Work Detail%%' OR etype LIKE 'Fund Raiser%%') 
        AND tstart BETWEEN '%s' AND '%s');
        """ % (id, start, end))

    #Gets all shifts for one person in a range.
    def get_shift_duration(self, id, start, end):
        return self.s_query("""
        SELECT shift_end-shift_start, bonus FROM shift 
        WHERE person_id = '%s' AND shift_end BETWEEN '%s' AND '%s';
        """ % (id, start, end))

    def get_appar(self, id, start, end):
        return self.s_query("""
        SELECT COUNT(*) FROM event WHERE tstart BETWEEN '%s' AND '%s'
        AND (etype LIKE 'Work Detail - Sunday%%' OR etype LIKE 'Work Detail - Weekly%%' OR etype LIKE
        'Work Detail - Daily%%') AND id IN (SELECT event_id FROM person_xref_event WHERE
        person_id = '%s');""" % (start, end, id))

    # fix this when fundraisers are loaded
    def get_fundraisers(self, id, start, end):
        return self.s_query("""
        SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.id = pe.event_id
        AND e.etype LIKE 'Fund Raiser%%';""" % (id, start, end))

    def get_meetings(self, id, start, end):
        return self.s_query("""
        SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.id = pe.event_id
        AND e.etype LIKE 'Business Meetings%%';""" % (id, start, end))

    def get_trainings(self, id, start, end):
        return self.s_query("""
        SELECT e.tend-e.tstart, e.etype FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.etype LIKE 'training%%' AND e.tstart BETWEEN '%s'
        AND '%s' AND e.id = pe.event_id;""" % (id, start, end))

	#Returns the total number of calls over a specified date range on the admin page*/
    def dashboard_calls(self, start, end, station):
        return self.s_query("SELECT COUNT(*) FROM incident WHERE tstamp BETWEEN '%s' AND '%s';" % (start, end))[0][0]

    def dashboard_responders(self, start, end, station):
        totalCalls = self.dashboard_calls(start, end, station)	
        totalResponders = self.s_query("SELECT COUNT(*) FROM incident AS i, person_xref_incident AS ref WHERE i.id=ref.incident_id AND i.tstamp BETWEEN '%s' AND '%s';" % (start, end))[0][0]
        return totalResponders/totalCalls
    
    def delete(self, start, end):
        self.delete_incidents(start, end)
        self.delete_events(start, end)
        self.delete_classes(start, end)
    
    def delete_incidents(self, start, end):
        self.i_query("""
        DELETE FROM person_xref_incident WHERE incident_id IN 
        (SELECT id FROM incident WHERE tstamp BETWEEN '%s' AND '%s');
        """ % (start, end))

        self.i_query("""
        DELETE FROM incident WHERE tstamp BETWEEN '%s' AND '%s';
        """ % (start, end))

    def delete_classes(self, start, end):
        self.i_query("""
        DELETE FROM person_xref_class WHERE class_id IN
        (SELECT id FROM class WHERE tstart BETWEEN '%s' AND '%s');
        """ % (start, end))

        self.i_query("""
        DELETE FROM class WHERE tstart BETWEEN '%s' AND '%s';
        """ % (start, end))

    def delete_events(self, start, end):
        self.i_query("""
        DELETE FROM person_xref_event WHERE event_id IN
        (SELECT id FROM event WHERE tstart BETWEEN '%s' AND '%s');
        """ % (start, end))