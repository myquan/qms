from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import WeeklyReportForm, UploadFileForm, TaskForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from .models import Report, Task, Customer
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Create your views here.
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    return HttpResponse("You're looking at result")


@login_required
def index(request):
    my_date = datetime.date.today()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    reports4ThisWeek = Report.objects.filter(week=week_num)
    context = {'myreports': reports4ThisWeek}
    return render(request, 'weeklyReport/index.html', context)


@login_required
def historicalReport(request):
    my_date = datetime.date.today()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    reports4ThisWeek = Report.objects.all()
    context = {'myreports': reports4ThisWeek, 'name': 'jack'}
    return render(request, 'weeklyReport/index.html', context)


@login_required
def fillreport(request):
    if request.method == 'POST':
        form = WeeklyReportForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        # form = WeeklyReportForm({'your_name': request.user.first_name+' '+request.user.last_name})
        # form.fields['your_name'].error_messages = {'required':''}
        # self.fields['name'].error_messages = {'required': 'custom required message'}
        form = WeeklyReportForm()
    context = {'form': form}
    return render(request, 'weeklyReport/fillReport.html', context)


@login_required
def showReport(request, report_id):
    areport = Report.objects.get(pk=report_id)
    context = {'areport': areport}
    return render(request, 'weeklyReport/showReport.html', context)


@login_required
def uploadreport(request):
    if request.method == 'POST':
        form = WeeklyReportForm(request.POST)
        my_date = datetime.date.today()  # if date is 01/01/2018
        year, week_num, day_of_week = my_date.isocalendar()
        # print("Week #" + str(week_num) + " of year " + str(year))
        if form.is_valid():
            username = form.cleaned_data['your_name']
            username = request.user.username
            items_comingweek = form.cleaned_data['items_comingweek']
            items_lastweek = form.cleaned_data['items_lastweek']
            items_others = form.cleaned_data['others']
            newReport = Report(reporter=username, itemsLastWeek=items_lastweek, itemsComingWeek=items_comingweek,
                               lastUpdateTime=timezone.now(), year=year, week=week_num, others=items_others)
            newReport.save()
            # context = {'username': username, 'year': year, 'week': week_num}
            text_content = username + ' your report for Week ' + str(week_num) + ' at year ' + str(
                year) + ' was uploaded.'
            context = {'text_content': text_content}
            return render(request, 'weeklyReport/generalText.html', context)
    else:
        form = WeeklyReportForm()


def listReportFiles(request):
    path = os.path.join(settings.BASE_DIR, 'statics\\weeklyReports')
    # PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    # print(path)
    file_list = os.listdir(path)
    return render(request, 'weeklyReport/announcementFileList.html', {'files': file_list})


def viewDocReport(request):
    return render(request, 'weeklyReport/viewDocReport.html')


def upload_file(request):
    my_date = datetime.date.today()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    username = request.user.username
    if request.method == 'POST' and request.FILES['myfile']:
        my_date = datetime.date.today()  # if date is 01/01/2018
        year, week_num, day_of_week = my_date.isocalendar()
        username = request.user.username
        reportFile = request.FILES['myfile']
        fs = FileSystemStorage()
        name, extension = os.path.splitext(reportFile.name)
        targetFileName = 'statics/weeklyReports/report_' + username + '_' + str(year) + '_' + str(week_num) + extension
        if os.path.exists(targetFileName):
            fs.delete('statics/weeklyReports/report_' + username + '_' + str(year) + '_' + str(week_num) + extension)
        filename = fs.save(targetFileName, reportFile)
        # form = UploadFileForm(request.POST, request.FILES)
        uploaded_file_url = '/static/weeklyReports/report_' + username + '_' + str(year) + '_' + str(
            week_num) + extension
        context = {'username': username, 'year': year, 'week': week_num, 'uploaded_file_url': uploaded_file_url}
        return render(request, 'weeklyReport/uploadAnnouncementFile.html', context)
        # return HttpResponseRedirect('/success/url/')
    else:
        targetFileName = 'statics/weeklyReports/report_' + username + '_' + str(year) + '_' + str(week_num) + '.docx'
        if os.path.exists(targetFileName):
            fileExist = True
        else:
            print(targetFileName)
            fileExist = False
        form = UploadFileForm()
        context = {'username': username, 'year': year, 'week': week_num, 'form': form, 'fileExist': fileExist}
        return render(request, 'weeklyReport/uploadAnnouncementFile.html', context)


def show_tasks(request):
    allTasks = Task.objects.all().select_related()
    username = request.user.username
    my_date = datetime.date.today()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    tasks = []
    for task in allTasks:
        print(task.customer.customer_name)
        taskjson = {'id': task.id, 'taskName': task.taskName, 'description': task.description,
                    'progress': task.progress, 'customer': task.customer.customer_name,
                    'createTime': task.createTime, 'owner': task.owner}
        tasks.append(taskjson)
    taskData = {'data': tasks}

    context = {'username': username, 'year': year, 'week': week_num, 'taskData': taskData}
    return render(request, 'weeklyReport/tasks.html', context)


def manage_tasks(request):
    allTasks = Task.objects.filter(owner=request.user.username).select_related()
    count = allTasks.count()
    print(count)
    username = request.user.username
    my_date = datetime.date.today()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    tasks = []
    for task in allTasks:
        print(task.customer.customer_name)
        taskjson = {'id': task.id, 'taskName': task.taskName, 'description': task.description,
                    'progress': task.progress, 'customer': task.customer.customer_name,
                    'createTime': task.createTime}
        tasks.append(taskjson)
    taskData = {'data': tasks}

    context = {'username': username, 'year': year, 'week': week_num, 'taskData': taskData}
    return render(request, 'weeklyReport/manageTasks.html', context)


def getTasks(request):
    taskData = {'data': [
        {'id': 1, 'taskName': 'Oli Bob', 'progress': '12', 'customer': 'red', 'crDate': '22/05/1982'},
        {'id': 2, 'taskName': '測試2', 'progress': '33', 'description': '明文字', 'crDate': '22/05/1982'},
    ]}

    return JsonResponse(taskData)


def editTask(request, task_id):
    username = request.user.username
    print(username)
    task_tobe_edit = Task.objects.get(id=task_id)
    print(task_tobe_edit.taskName)
    form = TaskForm()
    form.fields['taskName'].initial = task_tobe_edit.taskName
    form.fields['description'].initial = task_tobe_edit.description
    form.fields['customer'].initial = task_tobe_edit.customer
    form.fields['progress'].initial = task_tobe_edit.progress
    context = {'owner': username, 'theTask': task_tobe_edit, 'form': form}
    return render(request, 'weeklyReport/editTask.html', context)


def deleteTask(request, task_id):
    username = request.user.username
    try:
        task2Del=Task.objects.get(pk=task_id, owner=username)
        task_name = task2Del.taskName
        print('here')
        task2Del.delete()
        context = {"text_content": "任務: [" + task_name + '] 已經被刪除!'}
        print('done')
    except:
        context = {"text_content": "你無權刪除該任務!"}


    return render(request, 'weeklyReport/generalText.html', context)

def updateTask(request):
    username = request.user.username
    if request.method == 'POST':
        form = TaskForm(request.POST)
        my_date = datetime.date.today()
        year, week_num, day_of_week = my_date.isocalendar()
        data = request.POST
        if form.is_valid():
            tid=data.get('task_id')
            task = Task.objects.get(id = tid)
            task.taskName = form.cleaned_data['taskName']
            task.description = form.cleaned_data['description']
            customerObj = Customer.objects.get(pk=form.cleaned_data['customer'].id)
            task.customer = customerObj
            task.progress = form.cleaned_data['progress']

            task.save()
            text_content = username + ', 任務: [' + task.taskName + '] 已更新。'
            context = {'text_content': text_content}
            return render(request, 'weeklyReport/generalText.html', context)
        else:
            return render(request, '/')
    else:
        # form = WeeklyReportForm({'your_name': request.user.first_name+' '+request.user.last_name})
        # form.fields['your_name'].error_messages = {'required':''}
        # self.fields['name'].error_messages = {'required': 'custom required message'}
        form = TaskForm()
        context = {'username': username}
        return render(request, 'weeklyReport/showTasks.html', context)


def creatTasks(request):
    username = request.user.username
    if request.method == 'POST':
        form = TaskForm(request.POST)
        my_date = datetime.date.today()  # if date is 01/01/2018
        year, week_num, day_of_week = my_date.isocalendar()
        # print("Week #" + str(week_num) + " of year " + str(year))
        if form.is_valid():
            username = request.user.username
            taskName = form.cleaned_data['taskName']
            description = form.cleaned_data['description']
            customer = form.cleaned_data['customer']
            task = Task(owner=username, taskName=taskName, description=description, lastUpdateTime=timezone.now(),
                        customer=form.cleaned_data['customer'],
                        createTime=timezone.now(), year=year, week=week_num, progress=form.cleaned_data['progress'])
            task.save()
            text_content = username + ', 任務: [' + taskName + '] 已建立成功。'
            context = {'text_content': text_content}
            return render(request, 'weeklyReport/generalText.html', context)
        else:
            return render(request, '/')
    else:
        # form = WeeklyReportForm({'your_name': request.user.first_name+' '+request.user.last_name})
        # form.fields['your_name'].error_messages = {'required':''}
        # self.fields['name'].error_messages = {'required': 'custom required message'}
        form = TaskForm()
    context = {'username': username, 'form': form}
    return render(request, 'weeklyReport/createTask.html', context)
