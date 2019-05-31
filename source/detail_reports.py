import dbconnect

class Event_Detail_Report():
    def __init__(self, empNum, startTime, endTime, reportType):
        self.empNum = empNum
        self.startTime = startTime
        self.endTime = endTime
        self.reportType = reportType
        self.csvRows = []
        self.headerRow = ['Event Type', 'Start Time', 'End Time']
        self.connection = dbconnect.dbconnect()
        self.compute_detail_report()

    def compute_detail_report(self):
        data = []
        if self.reportType == "Training":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'training%')
        elif self.reportType == "Work Detail":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'work detail%')
        elif self.reportType == "Sundays & Weeklies":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'work detail-daily')
            data2 = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'work detail-weekly')
            data3 = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'work detail-sunday')
            if data == None:
                data = []
            if data2 != None:
                for dat in data2:
                    data.append(dat)
            if data3 != None:
                for dat in data3:
                    data.append(dat)                    
        elif self.reportType == "Fundraisers":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'work detail-fundraiser')
        elif self.reportType == "Business Meetings":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'business-meeting')
        if data != None:
            for event in data:
                row = []
                row.append(event[2])
                row.append(event[0])
                row.append(event[1])
                self.csvRows.append(row)
        self.connection.close()
        