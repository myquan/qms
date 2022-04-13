from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import UploadFileForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
#from .models import Report, Task, Customer
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.



@login_required
def index(request):
    my_date = datetime.date.today()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    context = {'myreports': 'io'}
    return render(request, 'announce/index.html', context)


def upload_announce(request):
    my_date = datetime.date.today()  # if date is 01/01/2018
    year, week_num, day_of_week = my_date.isocalendar()
    username = request.user.username
    if request.method == 'POST' and request.FILES['myfile']:
        my_date = datetime.date.today()  # if date is 01/01/2018
        year, week_num, day_of_week = my_date.isocalendar()
        username = request.user.username
        uploadedFile = request.FILES['myfile']
        fs = FileSystemStorage()
        #@name, extension = os.path.splitext(uploadedFile.name)
        targetFileName = 'statics/announcements/'+ uploadedFile.name # path + fileName
        if os.path.exists(targetFileName):
            fs.delete('statics/announcements/'+uploadedFile.name)
        uploadedName = fs.save(targetFileName, uploadedFile)
        # form = UploadFileForm(request.POST, request.FILES)
        uploaded_file_url = '/static/announcements/' + uploadedFile.name
        context = {'username': username, 'file_url' : uploaded_file_url}
        return render(request, 'announce/alreadyUploaded.html', context)
    else:
        form = UploadFileForm()
        context = {'username': username, 'year': year, 'week': week_num, 'form': form}
        return render(request, 'announce/uploadAnnouncementFile.html', context)


def manage_announce(request):
    context = {'text_content': 'not ready, yet.'}
    return render(request, 'announce/generalText.html', context)


def listAnnouncementFiles(request):
    path = os.path.join(settings.BASE_DIR, 'statics\\announcements')
    # PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    # print(path)
    file_list = os.listdir(path)
    return render(request, 'announce/announcementFileList.html', {'files': file_list})

