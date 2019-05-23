from dbconnect import dbconnect

class Report():
    def __init__(self, empNum, startTime, endTIme):
        self.empNum = empNum
        self.startTime = startTime
        self.endTime = endTime
        self.lastName = ""
        self.firstName = ""
        self.rank = ""
        self.shifts = 0
        self.actCalls = 0
        self.totCalls = 0
        self.WDHours = 0
        self.apparatus = 0
        self.fundraisers = 0
        self.meetings = 0
        self.trainings = 0
        self.totTrainings = 0
        self.daysService = 0
        self.yrsService = 0
        self.connection = dbconnect()

    def compute_full_report(self):
        self.compute_shifts()
        self.compute_act_calls()
        self.compute_total_calls()
        self.compute_work_detail_hours()
        self.compute_apparatus()
        self.compute_fundraisers()
        self.compute_meetings()
        self.compute_trainings()
        self.compute_service()
        self.compute_employee_details()
        self.connection.close()

    def compute_shifts(self):
        shift = self.connection.s_query("""SELECT tend-tstart, tstart, tend FROM person_xref_shift
        WHERE person_id = '%s' AND tstart BETWEEN '%s' AND '%s';""" % (self.empNum, self.startTime, self.endTime))
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
        self.shifts = credit

    def compute_act_calls(self):
        calls = self.connection.s_query("""SELECT i.COUNT(*) FROM incident AS i, person_xref_incident AS pi
        WHERE pi.person_id = '%s' AND s.tstamp BETWEEN '%s' AND '%s';""" % (self.empNum, self.startTime, self.endTime))
        self.actCalls = calls

    def compute_total_calls(self):
        self.totCalls = self.actCalls + (2 * self.shifts)

    def compute_work_detail_hours(self):
        wdt = self.connection.s_query("""SELECT e.end-e.start, type FROM event AS e, person_xref_event
        AS pe WHERE pe.person_id = '%s' AND e.type LIKE 'work detail%' AND e.tstart BETWEEN '%s'
        AND '%s' AND pe.event_id = e.id;""" % (self.empNum, self.startTime, self.endTime))        
        wdthours = 0
        for w in wd:
            wdthours += w[0].seconds/3600
                
        self.WDHours = wdthours

    def compute_apparatus(self):
        self.apparatus = self.connection.s_query("""COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND pe.event_id = e.id
        AND (e.type = 'work detail-daily' OR e.type = 'work detail-weekly' OR e.type = 'work detail-sunday');""" % (self.empNum, self.startTime, self.endTime))

    def compute_fundraisers(self):
        self.fundraisers = self.connection.s_query("""COUNT(*) FROM event AS e, person_xref_event
        AS pe WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND pe.event_id = e.id
        AND e.type = 'work detail-fundraiser';""" % (self.empNum, self.startTime, self.endTime))

    def compute_meetings(self):
        self.meetings = self.connection.s_query("""SELECT e.COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.type = 'meeting' AND e.tstart BETWEEN '%s'
        AND '%s' AND pe.event_id = e.id;""" % (self.empNum, self.startTime, self.endTime))

    def compute_trainings(self):
        training = self.connection.s_query("""SELECT e.end-e.start, type FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.type LIKE 'training%' AND e.tstart BETWEEN '%s'
        AND '%s' AND pe.event_id = e.id;""" % (self.empNum, self.startTime, self.endTime))
        
        thours = 0
        tthours = 0
        for t in training:
            tthours += t[0].seconds/3600
            if t[1] == 'training-department':
                thours += t[0].seconds/3600
                
        self.totTrainings = tthours
        self.trainings = thours

    def compute_service():
        self.daysService = 1
        self.yrsService = 1

    def compute_employee_details():
        # querry database for employee first name, last name, and rank (resident or not)
        # do we want to add notes?
        print("")

        
