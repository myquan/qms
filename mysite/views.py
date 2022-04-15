from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from weeklyReport.models import Task
from announce.models import Announcement, ClockRecord
from datetime import datetime, timezone, tzinfo
from django.utils import timezone
import os
from django.conf import settings
from django.utils.safestring import SafeString

def Hello(request):
    if request.user.is_authenticated:
        # === 打卡 ===
        username = request.user.username

        allTasks = Task.objects.all().select_related()
        my_date = datetime.now()  # if date is 01/01/2018
        year, week_num, day_of_week = my_date.isocalendar()
        tasks = []
        for task in allTasks:
            taskjson = {'id': task.id, 'taskName': task.taskName, 'description': task.description,
                        'progress': task.progress, 'customer': task.customer.customer_name,
                        'createTime': task.create_time, 'owner': task.owner}
            tasks.append(taskjson)
        taskData = {'data': tasks}
        path = os.path.join(settings.BASE_DIR, 'statics\\announcements')
        file_list = os.listdir(path)
        announcements = []
        for item in Announcement.objects.all():
            item = {'file_name': item.file_name, 'announce_name': item.announce_name}
            announcements.append(item)
        today = datetime.now()  # if date is 01/01/2018
        clock_in = today
        year, week_num, day_of_week = my_date.isocalendar()
        today.replace(hour=7, minute=0)
        ip= get_client_ip(request)
        clock_out=True
        try:
            clockRecord = ClockRecord.objects.get(account_name=username)
            clock_in = clockRecord.create_time
        except:
            if ('192.168.1' in ip):
                clockRecord = ClockRecord(account_name=username)
                clockRecord.save()
                clock_out = False #打卡成功
            else:
                clock_out = True #不能由外部打卡
            clock_in = timezone.now()
        #zone_taipei = tz.gettz('Asia/Taipei')
        clock_in = timezone.localtime(clock_in)
        context = {'username': username, 'year': year, 'week': week_num, 'taskData': taskData, 'announcements': announcements, 'clock_in': clock_in, 'ip':ip, 'clock_out':clock_out}
        return render(request, 'main_index.html', context)
    else:
        return HttpResponseRedirect('/accounts/login/')


def norush(request):
    return render(request, 'polls/no-rush.html')


def faqs(request):
    return render(request, 'polls/faqs.html')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip