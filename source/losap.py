from source import dbconnect
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
        self.total_leave = 0
        leave_instances = self.connection.get_statuses(str(self.empNum))
        startDateTime = datetime.datetime.strptime(self.startTime, '%Y-%m-%d %H:%M:%S.%f')
        endDateTime = datetime.datetime.strptime(self.endTime, '%Y-%m-%d %H:%M:%S.%f')
        first_rel_ind = 0
        last_rel_ind = 0
        for change in leave_instances:
            if change[1] >= startDateTime and change[1] <= endDateTime:
                break
            first_rel_ind += 1
        if first_rel_ind > 0:
            first_rel_ind -= 1
        for change in leave_instances:
            if change[1] >= endDateTime:
                last_rel_ind += 1
                break
            last_rel_ind += 1
        relevant_instances = leave_instances[first_rel_ind:last_rel_ind + 1]
        i = 0
        x = len(relevant_instances) 
        while i < x:
            if relevant_instances[i][0] != "Active":
                if i+1 < x:
                    duration = relevant_instances[i+1][1] - relevant_instances[i][1]
                    days = duration.days
                    today = datetime.date.today()
                    if relevant_instances[i][1].year == today.year:
                        self.total_leave += (relevant_instances[i+1][1].date() - relevant_instances[i][1].date()).days
                    else:
                        self.total_leave += (relevant_instances[i+1][1].date() - datetime.date(today.year, 1, 1)).days
                    print(self.total_leave)
                    leave = Leave(relevant_instances[i][1].date(), relevant_instances[i+1][1].date(), days, relevant_instances[i][0], relevant_instances[i][3])
                    self.leave_instances.append(leave)
                else:
                    today = datetime.date.today()
                    duration = datetime.datetime.now() - relevant_instances[i][1]
                    days = duration.days
                    if relevant_instances[i][1].year == today.year:
                        self.total_leave += (today - relevant_instances[i][1].date()).days
                    else:
                        self.total_leave += (today - datetime.date(today.year, 1, 1)).days
                    print(self.total_leave)
                    leave = Leave(relevant_instances[i][1].date(), "Future", days, relevant_instances[i][0], relevant_instances[i][3])
                    self.leave_instances.append(leave)
            i += 1

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
