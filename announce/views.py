from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import AnnouncementForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from .models import Category_Announcement, Announcement, ClockRecord
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import Group

# Create your views here.


@login_required
def index(request):
    user = request.user
    print(user.groups)
    my_date = datetime.date.today()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    text_content = 'groups:<br>'
    if user.groups.filter(name='employee'):
        text_content += 'YES. '
    for group in user.groups.all():
        text_content += group.name+'<br>'
    context = {'text_content': text_content}
    return render(request, 'announce/generalText.html', context)


@login_required
def upload_announce(request):
    operation_name='新增管理部公告'
    my_date = datetime.now()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    username = request.user.username
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            is_file_available = request.FILES.get('myfile', False)
            if is_file_available:
                uploadedFile = request.FILES['myfile']
                fs = FileSystemStorage()
                uploadedFileName= uploadedFile.name
                targetFileName = 'statics/announcements/' + uploadedFile.name  # path + fileName
                if os.path.exists(targetFileName):
                    fs.delete('statics/announcements/' + uploadedFile.name)
                uploadedName = fs.save(targetFileName, uploadedFile)
            else:
                uploadedFileName="N.A."
            username = request.user.username
            # save to database
            announcement = Announcement(uploader=username, description=form.cleaned_data['description'])
            announcement.announce_name = form.cleaned_data['announcementName']
            announcement.file_name = uploadedFileName
            announcement.category = form.cleaned_data['category']
            announcement.save()
            # form = UploadFileForm(request.POST, request.FILES)
            uploaded_file_url = '/static/announcements/' + uploadedFileName
            context = {'username': username, 'file_url': uploaded_file_url}
            return render(request, 'announce/alreadyUploaded.html', context)
        else:
            return HttpResponseRedirect('/')
    else:
        form = AnnouncementForm()
        context = {'username': username, 'year': year, 'week': week_num, 'form': form, 'operation_name': operation_name}
        return render(request, 'announce/uploadAnnouncementFile.html', context)


@login_required
def upload_benefit(request): #上傳/新增福委公告
    username = request.user.username
    if request.method == 'POST' and request.FILES['myfile']:
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['announcementName'])
            username = request.user.username
            uploadedFile = request.FILES['myfile']
            fs = FileSystemStorage()
            targetFileName = 'statics/announcements/' + uploadedFile.name  # path + fileName
            if os.path.exists(targetFileName):
                fs.delete('statics/announcements/' + uploadedFile.name)
            uploadedName = fs.save(targetFileName, uploadedFile)
            # save to database
            announcement = Announcement(uploader=username, description=form.cleaned_data['description'])
            announcement.announce_name = form.cleaned_data['announcementName']
            announcement.file_name = uploadedFile
            announcement.category = form.cleaned_data['category']
            announcement.save()
            # form = UploadFileForm(request.POST, request.FILES)
            uploaded_file_url = '/static/announcements/' + uploadedFile.name
            context = {'username': username, 'file_url': uploaded_file_url}
            return render(request, 'announce/alreadyUploaded.html', context)
        else:
            return HttpResponseRedirect('/')
    else:
        form = AnnouncementForm()
        print('form.category')
        context = {'username': username, 'year': year, 'week': week_num, 'form': form}
        return render(request, 'announce/uploadAnnouncementFile.html', context)


@login_required
def update_announce(request):
    username = request.user.username
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['description'])
            aid = request.POST['aid']
            item_tobe_update = Announcement.objects.get(pk=aid)
            is_file_available = request.FILES.get('myfile', False)
            if is_file_available:
                uploadedFile = request.FILES['myfile']
                fs = FileSystemStorage()
                targetFileName = 'statics/announcements/' + uploadedFile.name  # path + fileName
                print(targetFileName)
                if os.path.exists(targetFileName):
                    fs.delete('statics/announcements/' + uploadedFile.name)
                uploadedName = fs.save(targetFileName, uploadedFile)
                item_tobe_update.file_name = uploadedFile.name
                uploaded_file_url = '/static/announcements/' + uploadedFile.name
            else:
                uploaded_file_url = '/static/announcements/' + item_tobe_update.file_name
            username = request.user.username
            item_tobe_update.uploader=username
            item_tobe_update.description=form.cleaned_data['description']
            item_tobe_update.announce_name = form.cleaned_data['announcementName']

            item_tobe_update.category = form.cleaned_data['category']
            item_tobe_update.save()
            # form = UploadFileForm(request.POST, request.FILES)
            #uploaded_file_url = '/static/announcements/' + uploadedFile.name
            context = {'username': username, 'file_url': uploaded_file_url}
            return render(request, 'announce/alreadyUploaded.html', context)
        else:
            return HttpResponseRedirect('/')
    else:
        form = AnnouncementForm()
        context = {'username': username, 'year': year, 'week': week_num, 'form': form}
        return render(request, 'announce/uploadAnnouncementFile.html')



@login_required
def manage_announce(request):
    context = {'text_content': 'not ready, yet.'}
    return render(request, 'announce/generalText.html', context)



@login_required
def listAnnouncementFiles(request):
    path = os.path.join(settings.BASE_DIR, 'statics\\announcements')
    # PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    # print(path)
    file_list = os.listdir(path)
    return render(request, 'announce/announcementFileList.html', {'files': file_list})


@login_required
def manage_announcements(request):
    groups = request.user.groups.all()
    categoryList = []
    for group in groups:
        print(group)
        if group.name == 'administration_dept':
            categoryList=[1,2,3,4,5]
        elif group.name == 'welfare_comittee':
            categoryList.append(5)
    print(categoryList)
    allAnnouncements = Announcement.objects.filter(category__in = categoryList).select_related()
    username = request.user.username
    announcements = []
    for item in allAnnouncements:
        announcementjson = {'id': item.id,'file_name': item.file_name, 'announcementName': item.announce_name, 'description': item.description,
                    'uploader': item.uploader, 'category': item.category.category_name,
                    'createTime': item.create_time}
        announcements.append(announcementjson)
    announcementData = {'data': announcements}
    announcementCategories =  Category_Announcement.objects.filter(pk__in = categoryList)
    context = {'username': username, 'announcementData': announcementData, 'announcementCategories': announcementCategories}
    return render(request, 'announce/manageAnnouncements.html', context)


@login_required
def delete_announcements(request, announce_id):

    try:
        item2Del=Announcement.objects.get(pk=announce_id)
        item_name = item2Del.announce_name
        fs = FileSystemStorage()
        targetFileName = 'statics/announcements/' + item2Del.file_name  # path + fileName
        print(targetFileName)
        if os.path.exists(targetFileName):
            fs.delete(targetFileName)
            print('done')
        item2Del.delete()
        context = {"text_content": "公告: [" + item_name + '] 已經被刪除!'}
    except:
        context = {"text_content": "你無權刪除該任務!"}


    return render(request, 'announce/generalText.html', context)



@login_required
def edit_announcements(request, announce_id):
    item_tobe_edit = Announcement.objects.get(id=announce_id)
    username = request.user.username
    form = AnnouncementForm()
    form.fields['announcementName'].initial= item_tobe_edit.announce_name
    form.fields['description'].initial= item_tobe_edit.description
    form.fields['category'].initial= item_tobe_edit.category
    uploader= item_tobe_edit.uploader
    file_name = item_tobe_edit.file_name

    context = {'uploader': uploader, 'file_name':file_name, 'theAnnouncement': item_tobe_edit, 'form': form}
    return render(request, 'announce/editAnnouncement.html', context)


def get_announcements(request, category_id):
    if (category_id==0):
        groups = request.user.groups.all()
        categoryList = []
        for group in groups:
            print(group)
            if group.name == 'administration_dept':
                categoryList = [1, 2, 3, 4, 5]
            elif group.name == 'welfare_comittee':
                categoryList.append(5)
        print(categoryList)
        allAnnouncements = Announcement.objects.filter(category__in=categoryList).select_related()
    else:
        allAnnouncements = Announcement.objects.filter(category= category_id).select_related()
    username = request.user.username
    announcements = []
    for item in allAnnouncements:
        announcementjson = {'id': item.id,'file_name': item.file_name, 'announcementName': item.announce_name, 'description': item.description,
                    'uploader': item.uploader, 'category': item.category.category_name, 'createTime': item.create_time}
        announcements.append(announcementjson)
    announcementData = {'data': announcements}
    return JsonResponse(announcementData)


def clock_in_list(request):
    today=datetime.now().replace(hour=7, minute=0)
    atoday= timezone.make_aware(today)
    todayList= ClockRecord.objects.filter(create_time__gte=atoday)
    listStr="<h3>本日簽到表</h3><br>"
    listStr+='<table class="table table-striped" width="500"><thead><tr><th class="col-md-3">姓名</th><th>時間</th></thead>'
    listStr+='<tbody>'
    for item in todayList:
        clockin_time = timezone.localtime(item.create_time)
        listStr+='<tr><td>'+item.account_name+'</td><td>' + clockin_time.strftime('%H:%M %d') + '</td></tr>'
    listStr+='</tbody></table>'
    context={'text_content': listStr}
    return render(request, 'announce/generalText.html', context)
