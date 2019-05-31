import dbconnect
import datetime

class LOSAP():
    def __init__(self, empNum, startTime, endTime):
        self.empNum = empNum
        self.startTime = startTime
        self.endTime = endTime
        self.lastName = ""
        self.firstName = ""
        self.title = ""
        self.resident = ""
        self.csvRows = []
        self.leave_instances = []
        self.total_leave = 0
        self.connection = dbconnect.dbconnect()
        self.headerRow = ['Rank', 'Emp #', 'Last Name', 'First Name',
                          'Leave Start', 'Leave End', 'Duration',
                          'Type', 'Notes']

    def compute_losap(self):
        self.compute_losap_information()
        self.compute_employee_details()
        self.populate_csv_rows()
        self.connection.close()

    def compute_losap_information(self):
        # create leave objects and tally total leave time
        print("Here is where we create leave objects")        

    def compute_employee_details(self):
        person = self.connection.get_person(str(self.empNum))
        if person != None:
            self.firstName = person[0][1]
            self.lastName = person[0][2]
            self.title = person[0][3]
            self.resident = person[0][4]

    def populate_csv_rows(self):
        rank = "%s-%s" %(self.title, self.resident)
        for leave in self.leave_instances:
            next_row = []
            next_row.append(rank)
            next_row.append(str(self.empNum))
            next_row.append(str(self.lastName))
            next_row.append(str(self.firstName))
            next_row.append(str(leave.startDate))
            next_row.append(str(leave.endDate))
            next_row.append(str(leave.duration))
            next_row.append(str(leave.type))
            next_row.append(str(leave.notes))
            self.csvRows.append(next_row)
        
class Leave():
    def __init__(self, startDate, endDate, duration, leaveType, notes):
        self.startDate = startDate
        self.endDate = endDate
        self.duration = duration
        self.type = leaveType
        self.notes = notes
