import dbconnect
import datetime

class Report():
    def __init__(self, empNum, startTime, endTime):
        self.empNum = empNum
        self.startTime = startTime
        self.endTime = endTime
        self.lastName = ""
        self.firstName = ""
        self.title = ""
        self.resident = ""
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
        self.connection = dbconnect.dbconnect()
        self.csvRow = []
        self.headerRow = ['Rank','Emp #','Last Name','First Name',
                          'Actual Calls', 'Shift Volunteer', 'Resident Volunteer',
                          'Work Detail Hours', 'Apparatus Checks', 'Training-Dept',
                          'Training-Total', 'Fundraiser', 'Business Meetings',
                          'Days of Service', 'Years of Service']

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
        self.create_csv_row()
        self.connection.close()

    def compute_shifts(self):
        shift = self.connection.s_query("""SELECT shift_end-shift_start, shift_start, shift_end FROM person_xref_shift
        WHERE person_id = '%s' AND shift_start BETWEEN '%s' AND '%s';""" % (self.empNum, self.startTime, self.endTime))
        credit=0
        counter=0
        if shift != None:
            for s in shift:
                hours = (s[0].seconds/3600) + (s[0].days * 24)
                credit += hours // 12                
                if hours>=3 and hours<11:
                    counter += hours
            credit += counter // 12
            self.shifts = int(credit)

    def compute_act_calls(self):
        calls = self.connection.s_query("""SELECT COUNT(*) FROM incident AS i, person_xref_incident AS pi
        WHERE pi.person_id = '%s' AND i.id = pi.incident_id AND i.tstamp BETWEEN '%s' AND '%s';""" % (self.empNum, self.startTime, self.endTime))
        if calls == None:
            self.actCalls = 0
        else:
            self.actCalls = calls[0][0]

    def compute_total_calls(self):
        self.totCalls = self.actCalls + (2 * self.shifts)

    def compute_work_detail_hours(self):
        wdt = self.connection.s_query("""
        SELECT e.tend-e.tstart, e.etype FROM event AS e, person_xref_event
        AS pe WHERE pe.person_id = '%s' AND e.etype LIKE 'work detail%%' AND e.tstart BETWEEN '%s'
        AND '%s' AND e.tstart = pe.tstart AND e.tend = pe.tend AND e.etype = pe.type;""" % (self.empNum, self.startTime, self.endTime))        
        wdthours = 0
        if wdt != None:
            for w in wdt:
                wdthours += (w[0].seconds/3600) + (w[0].days * 24)
                
        self.WDHours = wdthours

    def compute_apparatus(self):
        appar = self.connection.s_query("""SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.tstart = pe.tstart AND e.tend = pe.tend AND e.etype = pe.type
        AND (e.etype = 'work detail-daily' OR e.etype = 'work detail-weekly' OR e.etype = '
        work detail-sunday');""" % (self.empNum, self.startTime, self.endTime))
        if appar == None:
            self.apparatus = 0
        else:
            self.apparatus = appar[0][0]

    def compute_fundraisers(self):
        funds = self.connection.s_query("""SELECT COUNT(*) FROM event AS e, person_xref_event
        AS pe WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.tstart = pe.tstart AND e.tend = pe.tend AND e.etype = pe.type
        AND e.etype = 'work detail-fundraiser';""" % (self.empNum, self.startTime, self.endTime))
        if funds == None:
            self.fundraisers = 0
        else:
            self.fundraisers = funds[0][0]

    def compute_meetings(self):
        meets = self.connection.s_query("""SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.etype = 'meeting' AND e.tstart BETWEEN '%s'
        AND '%s' AND e.tstart = pe.tstart AND e.tend = pe.tend AND e.etype = pe.type;""" % (self.empNum, self.startTime, self.endTime))
        if meets == None:
            self.meetings = 0
        else:
            self.meetings = meets[0][0]

    def compute_trainings(self):
        training = self.connection.s_query("""SELECT e.tend-e.tstart, e.etype FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.etype LIKE 'training%%' AND e.tstart BETWEEN '%s'
        AND '%s' AND e.tstart = pe.tstart AND e.tend = pe.tend AND e.etype = pe.type;""" % (self.empNum, self.startTime, self.endTime))
        
        thours = 0
        tthours = 0
        if training != None:
            for t in training:
                tthours += t[0].seconds/3600
                if t[1] == 'training-department':
                    thours += t[0].seconds/3600
                
            self.totTrainings = tthours
            self.trainings = thours

    def compute_service(self):
        statuses = self.connection.s_query("""SELECT status, to_char(date_change, 'YYYY-MM-DD HH:MI:SS') FROM person_status WHERE person_id = '%s';""" % (self.empNum))
        
        #start date, last change date, and current status, respectively
        sd = datetime.datetime.strptime(statuses[0][1], '%Y-%m-%d %H:%M:%S')
        lc = sd
        cs = 'Active'
        
        self.daysService = 0
        
        for s in statuses:
            
            if cs == 'Active' or cs == 'Medical':
                delta = datetime.datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S') - lc
                self.daysService += delta.days
                lc = datetime.datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S')
                cs = s[0]
            else:
                lc = datetime.datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S')
                cs = s[0]
                
            #This line converts the timestamp string to a python datetime!
            #datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S')
        if cs == 'Active' or cs == 'Medical':
            delta = datetime.datetime.now() - lc
            self.daysService += delta.days
            
        self.yrsService = float("%0.2f" % (self.daysService / 365.0))
        

    def compute_employee_details(self):
        # querry database for employee first name, last name, and rank (resident or not)
        # do we want to add notes?
        person = self.connection.get_person(str(self.empNum))
        if person != None:
            self.firstName = person[0][1]
            self.lastName = person[0][2]
            self.title = person[0][3]
            self.resident = person[0][4]

    def create_csv_row(self):
        rank = "%s-%s" %(self.title, self.resident)
        self.csvRow.append(rank)
        self.csvRow.append(str(self.empNum))
        self.csvRow.append(str(self.lastName))
        self.csvRow.append(str(self.firstName))
        self.csvRow.append(str(self.actCalls))
        self.csvRow.append(str(self.shifts))
        self.csvRow.append(str(self.totCalls))
        self.csvRow.append(str(self.WDHours))
        self.csvRow.append(str(self.apparatus))
        self.csvRow.append(str(self.trainings))
        self.csvRow.append(str(self.totTrainings))
        self.csvRow.append(str(self.fundraisers))
        self.csvRow.append(str(self.meetings))
        self.csvRow.append(str(self.daysService))
        self.csvRow.append(str(self.yrsService))
