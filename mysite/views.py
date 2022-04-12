from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from weeklyReport.models import Task
import datetime
import os
from django.conf import settings


def Hello(request):
    if request.user.is_authenticated:
        allTasks = Task.objects.all().select_related()
        username = request.user.username
        my_date = datetime.date.today()  # if date is 01/01/2018
        year, week_num, day_of_week = my_date.isocalendar()
        tasks = []
        for task in allTasks:
            print(task.customer.customer_name)
            taskjson = {'id': task.id, 'taskName': task.taskName, 'description': task.description,
                        'progress': task.progress, 'customer': task.customer.customer_name,
                        'createTime': task.create_time, 'owner': task.owner}
            tasks.append(taskjson)
        taskData = {'data': tasks}
        path = os.path.join(settings.BASE_DIR, 'statics\\announcements')
        file_list = os.listdir(path)

        context = {'username': username, 'year': year, 'week': week_num, 'taskData': taskData, 'files': file_list}
        return render(request, 'main_index.html', context)
    else:
        return HttpResponseRedirect('/accounts/login/')


def norush(request):
    return render(request, 'polls/no-rush.html')


def faqs(request):
    return render(request, 'polls/faqs.html')

