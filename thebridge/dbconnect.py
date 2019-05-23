
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
        #This is not done
        shift = self.s_query("""SELECT tend-tstart, tstart, tend FROM person_xref_shift
        WHERE person_id = '%s' AND tstart BETWEEN '%s' AND '%s';""" % (empNum, startTime, endTime))
        credit=0
        counter=0
        for s in shift:
            hours = s[0].seconds/3600
            if hours >= 11 and hours<= 13:
                credit+=1
            elif hours>=23 and hours<=25:
                credit+=2
                #Insert code for holiday and weekend here
            elif hours>=3 and hours<11:
                counter += hours
        credit += int(counter/12)

        actCalls = self.s_query("""SELECT i.COUNT(*) FROM incident AS i, person_xref_incident AS pi
        WHERE pi.person_id = '%s' AND s.tstamp BETWEEN '%s' AND '%s';""" % (empNum, startTime, endTime))

        totCalls = (2*credit) + actcalls

        meetings = self.s_query("""SELECT e.COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.type = 'meeting' AND e.tstart BETWEEN '%s'
        AND '%s' AND pe.event_id = e.id;""" % (empNum, startTime, endTime))

        training = self.s_query("""SELECT e.end-e.start, type FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.type LIKE 'training%' AND e.tstart BETWEEN '%s'
        AND '%s' AND pe.event_id = e.id;""" % (empNum, startTime, endTime))
        
        thours = 0
        tthours = 0
        for t in training:
            tthours += t[0].seconds/3600
            if t[1] == 'training-department':
                thours += t[0].seconds/3600
                
        totTrainings = tthours
        trainings = thours
        
        
        wdt = self.s_query("""SELECT e.end-e.start, type FROM event AS e, person_xref_event
        AS pe WHERE pe.person_id = '%s' AND e.type LIKE 'work detail%' AND e.tstart BETWEEN '%s'
        AND '%s' AND pe.event_id = e.id;""" % (empNum, startTime, endTime))
        
        wdthours = 0
        for w in wd:
            wdthours += w[0].seconds/3600
                
        WDHours = wdthours

        fundraisers = self.s_query("""COUNT(*) FROM event AS e, person_xref_event
        AS pe WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND pe.event_id = e.id
        AND e.type = 'work detail-fundraiser';""" % (empNum, startTime, endTime))

        apparatus = self.s_query("""COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND pe.event_id = e.id
        AND (e.type = 'work detail-daily' OR e.type = 'work detail-weekly' OR e.type = 'work detail-sunday');""" % (empNum, startTime, endTime))        

        dos = 0
        yos = dos / 365
        return Report(credit, actCalls, totCalls, WDHours, apparatus, fundraisers, meetings, trainings, totTrainings, dos, yos)
