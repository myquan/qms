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
        #path = os.path.join(settings.BASE_DIR, 'statics\\announcements')
        #file_list = os.listdir(path)
        #=== 管理部公告 ===
        announcements = []
        for item in Announcement.objects.exclude(category=5):
            localUpdateTime = timezone.localtime(item.update_time)
            itemJson = {'file_name': item.file_name, 'announce_name': item.announce_name, 'update_time': localUpdateTime.strftime("%m/%d %H:%M")}
            announcements.append(itemJson)
        #=== 福委公告 ===
        welfareData = []
        for item in Announcement.objects.filter(category=5):
            localUpdateTime = timezone.localtime(item.update_time)
            itemJson = {'file_name': item.file_name, 'announce_name': item.announce_name, 'update_time': localUpdateTime.strftime("%m/%d %H:%M")}
            welfareData.append(itemJson)

        #=== 簽到作業 ===
        today = datetime.now()  # if date is 01/01/2018
        clock_in = today
        year, week_num, day_of_week = my_date.isocalendar()
        today=today.replace(hour=7, minute=0)
        atoday=timezone.make_aware(today)
        ip= get_client_ip(request)
        clock_out=True
        #clockRecord = ClockRecord.objects.filter(account_name=username, create_time__gte=atoday)
        print(atoday)
        try:
            clockRecord = ClockRecord.objects.filter(account_name=username, create_time__gte=atoday)
            print('print')
            clock_in = clockRecord[0].create_time
            #print(clock_in)
            clock_out=False
        except:
            print('except')
            if ('192.168.1' in ip):
                clockRecord = ClockRecord(account_name=username)
                clockRecord.save()
                clock_out = False #打卡成功
            else:
                clock_out = True #不能由外部打卡
            clock_in = timezone.now()
        #zone_taipei = tz.gettz('Asia/Taipei')
        clock_in = timezone.localtime(clock_in)
        context = {'username': username, 'year': year, 'week': week_num, 'taskData': taskData, 'announcements': announcements, 'welfareData': welfareData, 'clock_in': clock_in, 'ip':ip, 'clock_out':clock_out}
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