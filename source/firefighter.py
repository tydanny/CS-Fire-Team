#firefighter.py
from stats import Stats

class Firefighter:
    
    #constructor
    def __init__(self, fname, lname, num, title, residency):
        self.fname = fname
        self.lname = lname
        self.empNum = num
        self.title = title
        self.residency = residency
        self.trainingHours = 0
        self.shifts = 0
        self.actualCalls = 0
        self.workDetail = 0
        self.apparatusChecks = 0
        self.fundraisers = 0
        self.meetings = 0

    def setTraining(self):
        self.trainingHours = Stats.getTrainingHours(self.empNum)

    def setShifts(self):
        self.shifts = Stats.getShifts(self.empNum)

    def setActCalls(self):
        self.actualCalls = Stats.getCalls(self.empNum)

    def setWorkDetail(self):
        self.workDetail = Stats.getWorkDetail(self.empNum)

    def setApparatusChecks(self):
        self.weeklies = Stats.getApparatusChecks(self.empNum)

    def setFundraisers(self):
        self.fundraisers = Stats.getFundraisers(self.empNum)

    def setMeetings(self):
        self.meetings = Stats.getMeetings(self.empNum)

    
