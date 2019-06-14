"""
This file contatins the Requirements enum which is used by the Report class.
The report class is used to create all reports requested in the reports tab.
The class uses dbconnect functions to query the database and compile all
necessary information needed to create a report csv. 
"""
from source import dbconnect
import datetime
from enum import Enum

"""
Enum that stores criteria that personnel status should be graded against
"""
class Requirements(Enum):
    TRAININGS = 60
    SHIFTS = 36
    ACTUAL_CALLS = 54
    TOTAL_CALLS = 72
    WORK_DETAIL_HOURS = 36
    APPARATUS = 12
    FUNDRAISERS = 1
    MEETINGS = 6

"""
This class is used to compile all of the stats needed for a report for
one individual firefighter. The constructor takes in the person's employee
number and the start and end times for which the report should be computed.
The compute_full_report() function calls all of the helper methods to
populate the report's data members. Once the report has been computed,
the relevant data is stored in a list of strings in self.csvRow. The order
of the data in this list matches the labels in self.headerRow. These lists
can be easily written to a csv file to create a report. 
"""
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
        self.bonusShifts = 0
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
        self.trainingBehind = 0
        self.shiftBehind = 0
        self.callsBehind = 0
        self.wdBehind = 0
        self.apparatusBehind = 0
        self.fundraiserBehind = 0
        self.meetingsBehind = 0
        self.trainingRemain = 0
        self.shiftRemain = 0
        self.callsRemain = 0
        self.wdRemain = 0
        self.apparatusRemain = 0
        self.fundraiserRemain = 0
        self.meetingsRemain = 0
        self.totalComp = 0
        self.totalBehind = 0
        self.totalRemain = 0
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
                          'Actual Calls', 'Actual Shifts', 'Bonus Shifts', 'Shift Volunteer', 'Resident Volunteer',
                          'Work Detail Hours', 'Sundays & Weeklies', 'Training-Dept',
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
        self.compute_employee_status()
        self.create_csv_row()
        self.connection.close()
    """
    Counts up shifts and bonus shifts using the following criteria:
    1) If a shift's type is "Event", the person gets 1 shift credit
    2) If a shift is > 11 hours long, the person gets shift credit
       equal to the (shift duration) + (1 hour wiggle room) / (12)
       rounded down.
    3) If a shift lasts between 3 and 11 hours, the duration is added
       to a counter to be counted as AWS credit.
    4) If a shift lasts at least 3 hours past a multiple of 12 but not
       long enough to earn another shift, the excess is counted as AWS.
    5) Bonus shifts consist of shifts flagged as Weekends, ACO, or Holliday.
    6) Each Weekend shift adds one bonus shift to the counter unless 6
       bonus weekend shifts have already been encountered. There is
       currently no way to tell if two weekend bonus shifts were earned on
       the same weekend through a 48-hour shift.
    7) Each 12 hours of a shift marked ACO counts as a bonus shift with 1
       hour of wiggle room.
    8) Each shift flagged as a Holliday counts as 2 bonus shifts. 
    """
    def compute_shifts(self):
        shift = self.connection.get_shift_duration(str(self.empNum), self.startTime, self.endTime)
        credit=0
        counter=0
        self.bonusShifts = 0
        weekends = 0
        if shift != None:
            for s in shift:
                if s[1] == "Event":
                    credit += 1
                else:
                    hours = (s[0].seconds/3600) + (s[0].days * 24)
                    credit += (hours + 1) // 12   # 1 hour wiggle room
                    if hours % 12 >= 3 and hours % 12 < 11:
                        counter += (hours % 12)
                    if s[1] == "Weekend" and weekends < 6:
                        self.bonusShifts += 1
                        weekends += 1
                    if s[1] == "ACO":
                        self.bonusShifts += (hours + 1) // 12
                    if s[1] == "Holliday":
                        self.bonusShifts += 2
            credit += counter // 12
            self.shifts = int(credit)
    """
    The following few functions simply call dbconnect functions and add the
    data returned to the appropriate data member.
    """
    def compute_act_calls(self):
        calls = self.connection.get_num_actual_calls(str(self.empNum), self.startTime, self.endTime)
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
                wdthours += w[0]
        
        self.WDHours = wdthours

    def compute_apparatus(self):
        appar = self.connection.get_appar(self.empNum, self.startTime, self.endTime)
        if appar == None:
            self.apparatus = 0
        else:
            self.apparatus = appar[0][0]

    def compute_fundraisers(self):
        funds = self.connection.get_fundraisers(self.empNum, self.startTime, self.endTime)
        if funds == None:
            self.fundraisers = 0
        else:
            self.fundraisers = funds[0][0]

    def compute_meetings(self):
        meets = self.connection.get_meetings(self.empNum, self.startTime, self.endTime)
        if meets == None:
            self.meetings = 0
        else:
            self.meetings = meets[0][0]

    def compute_trainings(self):
        training = self.connection.get_classes(self.empNum, self.startTime, self.endTime)        
        thours = 0
        tthours = 0
        if training != None:
            for t in training:
                tthours += t[1]
                if "DEPT TRNG" in t[0]:
                    thours += t[1]
                
            self.totTrainings = tthours
            self.trainings = thours
    """
    Computes days and years of service. If the person has not resigned or retired,
    this is calculated by subtracting the persons hire date from the current date.
    If the person has retired or resigned, this is calculated by subracting the hire
    date from the date of the person's last status change. The person's hire date is
    the date corresponding to the person's first Active status recorded in our database.
    This can be changed manually through the personnel tab on the website. 
    """
    def compute_service(self):
        self.daysService = 0
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
    """
    Computes the person's status through tracking progress towards meeting each of their
    requirements for the current year. Uses the current date to figure out the percentage
    of the year that has passed and compute target values for each of the requirements based
    on this percentage. Compares the person's progress to these values to determine their
    status with respect to each requirement. For each individual status, the person is
    behind schedule if they are at least 15% behind where they should be with the requirement.
    They are falling behind if they are between 5% and 15% behind on the requirement. They are
    marked as complete once the requirement is completed and they are on-track otherwise.
    Fundraiser statusese are computed based on time of the year not based on percentage
    completion. A person's overall status is behind schedule if they are behind schedule towards
    at least three requirements. They are falling behind if they are behind in on or two
    requirements or are falling behind in any requirements. They are complete if all requirements
    have been completed and are on-track otherwise.
    """
    def compute_employee_status(self):
        curr = datetime.datetime.now(tz=None)
        daysPassed = (datetime.date.today() - datetime.date(curr.year, 1, 1)).days
        tarRatio = daysPassed / 365
        ratTrainings = self.trainings / Requirements.TRAININGS.value
        ratShifts = (self.shifts + self.bonusShifts) / Requirements.SHIFTS.value
        ratActCalls = self.actCalls / Requirements.ACTUAL_CALLS.value
        ratWorkDeets = self.WDHours / Requirements.WORK_DETAIL_HOURS.value
        ratApparatus = self.apparatus / Requirements.APPARATUS.value
        ratMeets = self.meetings / Requirements.MEETINGS.value

        self.trainingBehind = (tarRatio * Requirements.TRAININGS.value) - float(self.trainings)
        self.trainingRemain = Requirements.TRAININGS.value - self.trainingBehind - float(self.trainings)

        self.shiftBehind = (tarRatio * Requirements.SHIFTS.value) - self.shifts - self.bonusShifts
        self.shiftRemain = Requirements.SHIFTS.value - self.shiftBehind - float(self.shifts) - float(self.bonusShifts)

        self.callsBehind = (tarRatio * Requirements.ACTUAL_CALLS.value) - float(self.actCalls)
        self.callsRemain = Requirements.ACTUAL_CALLS.value - self.callsBehind - float(self.actCalls)

        self.wdBehind = (tarRatio * Requirements.WORK_DETAIL_HOURS.value) - float(self.WDHours)
        self.wdRemain = Requirements.WORK_DETAIL_HOURS.value - self.wdBehind - float(self.WDHours)
		
        self.apparatusBehind = (tarRatio * Requirements.APPARATUS.value) - float(self.apparatus)
        self.apparatusRemain = Requirements.APPARATUS.value - self.apparatusBehind - float(self.apparatus)
		
        self.meetingsBehind = (tarRatio * Requirements.MEETINGS.value) - float(self.meetings)
        self.meetingsRemain = Requirements.MEETINGS.value - self.meetingsBehind - float(self.meetings)
		
        chartTrain = float(self.trainings)
        chartShifts = float(self.shifts + self.bonusShifts)
        chartCalls = float(self.actCalls)
        chartWD = float(self.WDHours)
        chartApparatus = float(self.apparatus)
        chartFundraiser = float(self.fundraisers)
        chartMeetings = float(self.meetings)

        if tarRatio - 0.15 >= ratTrainings:
            self.statTrainings = "Behind-Schedule"
        elif tarRatio - 0.05 >= ratTrainings:
            self.statTrainings = "Falling-Behind"
        elif ratTrainings >= 0.99:
            self.statTrainings = "Complete"
            self.trainingBehind = 0
            self.trainingRemain = 0
            chartTrain = Requirements.TRAININGS.value
        else:
            self.trainingBehind = 0
            self.trainingRemain = Requirements.TRAININGS.value - float(self.trainings)

        if "Non-Resident" not in self.resident:
            self.statShifts = "Complete"
            self.shiftBehind = 0
            self.shiftRemain = 0
        elif tarRatio - 0.15 >= ratShifts:
            self.statShifts = "Behind-Schedule"
        elif tarRatio - 0.05 >= ratShifts:
            self.statShifts = "Falling-Behind"
        elif ratTrainings >= 0.99:
            self.statShifts = "Complete"
            self.shiftBehind = 0
            self.shiftRemain = 0
            chartShifts = Requirements.SHIFTS.value
        else:
            self.shiftBehind = 0
            self.shiftRemain = Requirements.SHIFTS.value - float(self.shifts) - float(self.bonusShifts)

        if "Non-Resident" in self.resident:
            self.statActCalls = "Complete"
            self.callsBehind = 0
            self.callsRemain = 0
        elif tarRatio - 0.15 >= ratActCalls:
            self.statActCalls = "Behind-Schedule"
        elif tarRatio - 0.05 >= ratActCalls:
            self.statActCalls = "Falling-Behind"
        elif ratActCalls >= 0.99:
            self.statActCalls = "Complete"
            self.callsBehind = 0
            self.callsRemain = 0
            chartCalls = Requirements.ACTUAL_CALLS.value
        else:
            self.callsBehind = 0
            self.callsRemain = Requirements.ACTUAL_CALLS.value - float(self.actCalls)

        if tarRatio - 0.1 >= ratWorkDeets:
            self.statWorkDeets = "Behind-Schedule"
        elif tarRatio - 0.01 >= ratWorkDeets:
            self.statWorkDeets = "Falling-Behind"
        elif ratWorkDeets >= 0.99:
            self.statWorkDeets = "Complete"
            self.wdBehind = 0
            self.wdRemain = 0
            chartWD = Requirements.WORK_DETAIL_HOURS.value
        else:
            self.wdBehind = 0
            self.wdRemain = Requirements.WORK_DETAIL_HOURS.value - float(self.WDHours)

        if tarRatio - 0.15 >= ratApparatus:
            self.statApparatus = "Behind-Schedule"
        elif tarRatio - 0.05 >= ratApparatus:
            self.statApparatus = "Falling-Behind"
        elif ratApparatus >= 0.99:
            self.statApparatus = "Complete"
            self.apparatusBehind = 0
            self.apparatusRemain = 0
            chartApparatus = Requirements.APPARATUS.value
        else:
            self.apparatusBehind = 0
            self.apparatusRemain = Requirements.APPARATUS.value- float(self.apparatus)

        if tarRatio - 0.15 >= ratMeets:
            self.statMeets = "Behind-Schedule"
        elif tarRatio - 0.05 >= ratMeets:
            self.statMeets = "Falling-Behind"
        elif ratMeets >= 0.99:
            self.statMeets = "Complete"
            self.meetingsBehind = 0
            self.meetingsRemain = 0
            chartMeetings = Requirements.MEETINGS.value
        else:
            self.meetingsBehind = 0
            self.meetingsRemain = Requirements.MEETINGS.value - float(self.meetings)

        if self.fundraisers >= 1:
            self.statFunds = "Complete"
            self.fundraiserBehind = 0
            self.fundraiserRemain = 0
            chartFundraiser = 1
        elif curr.month == 8 or curr.month == 9:
            self.statFunds = "Falling-Behind"
            self.fundraiserBehind = 1
            self.fundraiserRemain = 0
        elif curr.month >= 10:
            self.statFunds = "Behind-Schedule"
            self.fundraiserBehind = 1
            self.fundraiserRemain = 0
        else:
            self.fundraiserBehind = 0
            self.fundraiserRemain = 1
        
        if "Non-Resident" in self.resident:
            totalRequired = Requirements.TRAININGS.value + Requirements.SHIFTS.value + Requirements.WORK_DETAIL_HOURS.value + Requirements.APPARATUS.value + Requirements.MEETINGS.value + 1
            self.totalBehind = self.trainingBehind + self.shiftBehind + self.wdBehind + self.apparatusBehind + self.fundraiserBehind + self.meetingsBehind
            self.totalComp = chartTrain + chartShifts + chartWD + chartApparatus + chartFundraiser + chartMeetings
        else:
            totalRequired = Requirements.TRAININGS.value + Requirements.ACTUAL_CALLS.value + Requirements.WORK_DETAIL_HOURS.value + Requirements.APPARATUS.value + Requirements.MEETINGS.value + 1
            self.totalBehind = self.trainingBehind + self.callsBehind + self.wdBehind + self.apparatusBehind + self.fundraiserBehind + self.meetingsBehind
            self.totalComp = chartTrain + chartCalls + chartWD + chartApparatus + chartFundraiser + chartMeetings

        self.totalRemain = totalRequired - self.totalComp - self.totalBehind

        stats = []
        stats.append(self.statTrainings)
        stats.append(self.statShifts)
        stats.append(self.statActCalls)
        stats.append(self.statWorkDeets)
        stats.append(self.statApparatus)
        stats.append(self.statMeets)
        stats.append(self.statFunds)
        completed = True
        numBehind = 0
        numPartBehind = 0
        for stat in stats:
            if stat == "Behind-Schedule":
                numBehind += 1
                completed = False
            if stat == "Falling-Behind":
                numPartBehind += 1
                completed = False
            if stat == "On-Track":
                completed = False
        if completed:
            self.statOverall = "Complete"
        elif numBehind >= 3:
            self.statOverall = "Behind-Schedule"
        elif numBehind == 2 or numBehind == 1 or numPartBehind > 0:
            self.statOverall = "Falling-Behind"
        else:
            self.statOverall = "On-Track"
    """
    Adds gathered data to the csvRow data member to allow for easy addition
    to a csv file. Order shoulf match the order of the headerRow. 
    """
    def create_csv_row(self):
        rank = "%s-%s" %(self.title, self.resident)
        self.csvRow.append(rank)
        self.csvRow.append(str(self.empNum))
        self.csvRow.append(str(self.lastName))
        self.csvRow.append(str(self.firstName))
        self.csvRow.append(str(self.statOverall))
        self.csvRow.append(str(self.actCalls))
        self.csvRow.append(str(self.shifts))
        self.csvRow.append(str(self.bonusShifts))
        self.csvRow.append(str(self.shifts + self.bonusShifts))
        self.csvRow.append(str(self.totCalls))
        self.csvRow.append(str(self.WDHours))
        self.csvRow.append(str(self.apparatus))
        self.csvRow.append(str(self.trainings))
        self.csvRow.append(str(self.totTrainings))
        self.csvRow.append(str(self.fundraisers))
        self.csvRow.append(str(self.meetings))
        self.csvRow.append(str(self.daysService))
        self.csvRow.append(str(self.yrsService))
