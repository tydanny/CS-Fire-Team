from source import dbconnect
import datetime
from enum import Enum

class Requirements(Enum):
    TRAININGS = 60
    SHIFTS = 36
    ACTUAL_CALLS = 54
    TOTAL_CALLS = 72
    WORK_DETAIL_HOURS = 36
    APPARATUS = 12
    FUNDRAISERS = 1
    MEETINGS = 6

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
        self.statTrainings = "On-Track"
        self.statShifts = "On-Track"
        self.statActCalls = "On-Track"
        self.statWorkDeets = "On-Track"
        self.statApparatus = "On-Track"
        self.statFunds = "On-Track"
        self.statMeets = "On-Track"
        self.statOverall = "On-Track"
        self.csvRow = []
        self.headerRow = ['Rank','Emp #','Last Name','First Name', 'Completion Status',
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
        #TODO:FIX COMPUTE SERVICE
        #self.compute_service()
        self.compute_employee_details()
        self.compute_employee_status()
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
        wdt = self.connection.get_wdt(str(self.empNum), self.startTime, self.endTime)
        wdthours = 0
        if wdt != None:
            for w in wdt:
                wdthours += (w[0].seconds/3600) + (w[0].days * 24)
        
        self.WDHours = wdthours

    def compute_apparatus(self):
        appar = self.connection.s_query("""SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.id = pe.event_id
        AND (e.etype = 'work detail-daily' OR e.etype = 'work detail-weekly' OR e.etype = '
        work detail-sunday');""" % (self.empNum, self.startTime, self.endTime))
        if appar == None:
            self.apparatus = 0
        else:
            self.apparatus = appar[0][0]

    def compute_fundraisers(self):
        funds = self.connection.s_query("""SELECT COUNT(*) FROM event AS e, person_xref_event AS pe 
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.id = pe.event_id
        AND e.etype = 'work detail-fundraiser';""" % (self.empNum, self.startTime, self.endTime))
        if funds == None:
            self.fundraisers = 0
        else:
            self.fundraisers = funds[0][0]

    def compute_meetings(self):
        meets = self.connection.s_query("""SELECT COUNT(*) FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.tstart BETWEEN '%s' AND '%s' AND e.id = pe.event_id
        AND e.etype = 'meeting';""" % (self.empNum, self.startTime, self.endTime))
        if meets == None:
            self.meetings = 0
        else:
            self.meetings = meets[0][0]

    def compute_trainings(self):
        training = self.connection.s_query("""SELECT e.tend-e.tstart, e.etype FROM event AS e, person_xref_event AS pe
        WHERE pe.person_id = '%s' AND e.etype LIKE 'training%%' AND e.tstart BETWEEN '%s'
        AND '%s' AND e.id = pe.event_id;""" % (self.empNum, self.startTime, self.endTime))
        
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
        self.daysService = 0
        print(self.empNum)
        hireDate = self.connection.get_start(str(self.empNum)).date()
        statuses = self.connection.get_statuses(str(self.empNum))
        lastStatus = statuses[-1]
        if lastStatus[0] == "Retired" or lastStatus[0] == "Resigned":
            self.daysService = (lastStatus[1].date() - hireDate).days
        else:
            today = datetime.date.today()
            self.daysService = (today - hireDate).days
        self.yrsService = float("%0.2f" % (self.daysService / 365.0))        

    def compute_employee_details(self):
        person = self.connection.get_person(str(self.empNum))
        if person != None:
            self.firstName = person[0][1]
            self.lastName = person[0][2]
            self.title = person[0][3]
            self.resident = person[0][4]

    def compute_employee_status(self):
        curr = datetime.datetime.now(tz=None)
        daysPassed = (datetime.date.today() - datetime.date(curr.year, 1, 1)).days
        tarRatio = daysPassed / 365
        ratTrainings = self.trainings / Requirements.TRAININGS.value
        ratShifts = self.shifts / Requirements.SHIFTS.value
        ratActCalls = self.actCalls / Requirements.ACTUAL_CALLS.value
        ratWorkDeets = self.WDHours / Requirements.WORK_DETAIL_HOURS.value
        ratApparatus = self.apparatus / Requirements.APPARATUS.value
        ratMeets = self.meetings / Requirements.MEETINGS.value

        if tarRatio - 0.1 >= ratTrainings:
            self.statTrainings = "Behind-Schedule"
        elif tarRatio - 0.01 >= ratTrainings:
            self.statTrainings = "Falling-Behind"
        elif ratTrainings >= 0.99:
            self.statTrainings = "Complete"

        if tarRatio - 0.1 >= ratShifts:
            self.statShifts = "Behind-Schedule"
        elif tarRatio - 0.01 >= ratShifts:
            self.statShifts = "Falling-Behind"
        elif ratTrainings >= 0.99:
            self.statShifts = "Complete"

        if tarRatio - 0.1 >= ratActCalls:
            self.statActCalls = "Behind-Schedule"
        elif tarRatio - 0.01 >= ratActCalls:
            self.statActCalls = "Falling-Behind"
        elif ratActCalls >= 0.99:
            self.statActCalls = "Complete"

        if tarRatio - 0.1 >= ratWorkDeets:
            self.statWorkDeets = "Behind-Schedule"
        elif tarRatio - 0.01 >= ratWorkDeets:
            self.statWorkDeets = "Falling-Behind"
        elif ratWorkDeets >= 0.99:
            self.statWorkDeets = "Complete"

        if tarRatio - 0.1 >= ratApparatus:
            self.statApparatus = "Behind-Schedule"
        elif tarRatio - 0.01 >= ratApparatus:
            self.statApparatus = "Falling-Behind"
        elif ratApparatus >= 0.99:
            self.statApparatus = "Complete"

        if tarRatio - 0.1 >= ratMeets:
            self.statMeets = "Behind-Schedule"
        elif tarRatio - 0.01 >= ratMeets:
            self.statMeets = "Falling-Behind"
        elif ratMeets >= 0.99:
            self.statMeets = "Complete"

        if self.fundraisers >= 1:
            self.statFunds = "Complete"
        elif curr.month == 8 or curr.month == 9:
            self.statFunds = "Falling-Behind"
        elif curr.month >= 10:
            self.statFunds = "Behind-Schedule"

        stats = []
        stats.append(self.statTrainings)
        stats.append(self.statShifts)
        stats.append(self.statActCalls)
        stats.append(self.statWorkDeets)
        stats.append(self.statApparatus)
        stats.append(self.statMeets)
        stats.append(self.statFunds)
        completed = True
        for stat in stats:
            if stat == "Behind-Schedule":
                self.statOverall = "Behind-Schedule"
                completed = False
                break
            if stat == "Falling-Behind":
                self.statOverall = "Falling-Behind"
                completed = False
            if stat == "On-Track":
                completed = False
        if completed:
            self.statOverall = "Complete"
            

    def create_csv_row(self):
        rank = "%s-%s" %(self.title, self.resident)
        self.csvRow.append(rank)
        self.csvRow.append(str(self.empNum))
        self.csvRow.append(str(self.lastName))
        self.csvRow.append(str(self.firstName))
        self.csvRow.append(str(self.statOverall))
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
