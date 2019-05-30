from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect
from report import Report
import datetime
import csv

# Create your views here.
def officer(request):
	template = loader.get_template('officer_reports.html')
	context = {}
	return HttpResponse(template.render(context, request))
	
def admin(request):
    connection = dbconnect()
    firstQuery = "SELECT fname FROM PERSON;"
    firsts = connection.s_query(firstQuery)
    lastQuery = "SELECT lname FROM PERSON;"
    lasts = connection.s_query(lastQuery)
    numsQuery = "SELECT id FROM PERSON;"
    nums = connection.s_query(numsQuery)
    connection.close()
    i = len(firsts)
    x = 0
    emps = []
    while x < i:
        empfirst = firsts[x][0]
        emplast = lasts[x][0]
        empNum = nums[x][0]
        emp = "%s, %s %s" % (emplast, empfirst, empNum)
        emps.append(emp)
        x += 1
    template = loader.get_template('admin_reports.html')
    context = {'employees' : emps}
    return HttpResponse(template.render(context, request))


def index(request):
    connection = dbconnect()
    firstQuery = "SELECT fname FROM PERSON;"
    firsts = connection.s_query(firstQuery)
    lastQuery = "SELECT lname FROM PERSON;"
    lasts = connection.s_query(lastQuery)
    numsQuery = "SELECT id FROM PERSON;"
    nums = connection.s_query(numsQuery)
    connection.close()
    i = len(firsts)
    x = 0
    emps = []
    while x < i:
        empfirst = firsts[x][0]
        emplast = lasts[x][0]
        empNum = nums[x][0]
        emp = "%s, %s %s" % (emplast, empfirst, empNum)
        emps.append(emp)
        x += 1
    template = loader.get_template('reports.html')
    context = {'employees' : emps}
    return HttpResponse(template.render(context, request))

def submit(request):
    try:
        startDate = request.POST["time-start"]
        startTime = "%s 00:00:00.00" % startDate
        endDate = request.POST["time-end"]
        currTime = str(datetime.datetime.now().time())
        endTime = "%s %s" % (endDate, currTime)
        reportType = request.POST["type"]
        staff = request.POST.getlist("staff")
        connection = dbconnect()
        reports = []
        if staff[0] == "Generate For All":
                numsQuery = "SELECT id FROM PERSON;"
                nums = connection.s_query(numsQuery)
                i = len(nums)
                empNums = []
                x = 0
                while x < i:
                        empNums.append(nums[x][0])
                        x += 1
                for emp in empNums:
                    report = Report(str(emp), startTime, endTime)
                    report.compute_full_report()
                    reports.append(report)
        elif len(staff) == 1:
            nums = [int(s) for s in staff[0].split() if s.isdigit()]
            empNum = nums[-1]
            report = Report(str(empNum), startTime, endTime)
            report.compute_full_report()
            reports.append(report)
        else:
            empNums = []
            for person in staff:
                nums = [int(s) for s in person.split() if s.isdigit()]
                empNums.append(nums[-1])
            for emp in empNums:
                report = Report(str(emp), startTime, endTime)
                report.compute_full_report()
                reports.append(report)
        connection.close()
        if len(reports) >= 1:
            csv_name = "Personnel_Report_%s_%s.csv" % (startDate, endDate)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % csv_name
            writer = csv.writer(response)
            writer.writerow(reports[0].headerRow)
            for report in reports:
                    writer.writerow(report.csvRow)
        return response
    except Exception as e:
        print(e)
        template = loader.get_template('admin_error.html')
        context = {}
        return HttpResponse(template.render(context, request))


def officer_submit(request):
    try:
        startDate = request.POST["time-start"]
        startTime = "%s 00:00:00.00" % startDate
        endDate = request.POST["time-end"]
        currTime = str(datetime.datetime.now().time())
        endTime = "%s %s" % (endDate, currTime)
        reportType = request.POST["type"]
        staff = request.POST.getlist("staff")
        connection = dbconnect()
        reports = []
        if staff[0] == "Generate For All":
                numsQuery = "SELECT id FROM PERSON;"
                nums = connection.s_query(numsQuery)
                i = len(nums)
                empNums = []
                x = 0
                while x < i:
                        empNums.append(nums[x][0])
                        x += 1
                for emp in empNums:
                    report = Report(str(emp), startTime, endTime)
                    report.compute_full_report()
                    reports.append(report)
        elif len(staff) == 1:
            nums = [int(s) for s in staff[0].split() if s.isdigit()]
            empNum = nums[-1]
            report = Report(str(empNum), startTime, endTime)
            report.compute_full_report()
            reports.append(report)
        else:
            empNums = []
            for person in staff:
                nums = [int(s) for s in person.split() if s.isdigit()]
                empNums.append(nums[-1])
            for emp in empNums:
                report = Report(str(emp), startTime, endTime)
                report.compute_full_report()
                reports.append(report)
        connection.close()
        if len(reports) >= 1:
            csv_name = "Personnel_Report_%s_%s.csv" % (startDate, endDate)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % csv_name
            writer = csv.writer(response)
            writer.writerow(reports[0].headerRow)
            for report in reports:
                    writer.writerow(report.csvRow)
        return response
    except Exception as e:
        print(e)
        template = loader.get_template('officer_error.html')
        context = {}
        return HttpResponse(template.render(context, request))

def admin_submit(request):
    try:
        startDate = request.POST["time-start"]
        startTime = "%s 00:00:00.00" % startDate
        endDate = request.POST["time-end"]
        currTime = str(datetime.datetime.now().time())
        endTime = "%s %s" % (endDate, currTime)
        reportType = request.POST["type"]
        staff = request.POST.getlist("staff")
        connection = dbconnect()
        reports = []
        if staff[0] == "Generate For All":
                numsQuery = "SELECT id FROM PERSON;"
                nums = connection.s_query(numsQuery)
                i = len(nums)
                empNums = []
                x = 0
                while x < i:
                        empNums.append(nums[x][0])
                        x += 1
                for emp in empNums:
                    report = Report(str(emp), startTime, endTime)
                    report.compute_full_report()
                    reports.append(report)
        elif len(staff) == 1:
            nums = [int(s) for s in staff[0].split() if s.isdigit()]
            empNum = nums[-1]
            report = Report(str(empNum), startTime, endTime)
            report.compute_full_report()
            reports.append(report)
        else:
            empNums = []
            for person in staff:
                nums = [int(s) for s in person.split() if s.isdigit()]
                empNums.append(nums[-1])
            for emp in empNums:
                report = Report(str(emp), startTime, endTime)
                report.compute_full_report()
                reports.append(report)
        connection.close()
        if len(reports) >= 1:
            csv_name = "Personnel_Report_%s_%s.csv" % (startDate, endDate)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % csv_name
            writer = csv.writer(response)
            writer.writerow(reports[0].headerRow)
            for report in reports:
                    writer.writerow(report.csvRow)
        return response
    except Exception as e:
        print(e)
        template = loader.get_template('admin_error.html')
        context = {}
        return HttpResponse(template.render(context, request))
