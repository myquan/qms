from django.urls import path

from . import views

app_name = 'weeklyReport'
urlpatterns = [
    path('', views.show_tasks, name='index'),
    path('fillReport/', views.fillreport, name='fillReport'),
    path('uploadWeeklyReport/', views.uploadreport, name='uploadReport'),
    path('showReport/<int:report_id>/', views.showReport, name='showReport'),
    path('historicalReport/', views.historicalReport, name='historical'),
    path('reportFiles/', views.listReportFiles, name='reportFiles'),
    path('viewDocReport/', views.viewDocReport, name='viewDocReport'),
    path('uploadReportFile/', views.upload_file, name= 'uploadReportFile'),
    path('showTasks/', views.show_tasks, name = 'showTask'),
    path('manageTasks/', views.manage_tasks, name = 'manageTask'),
    path('createTask/', views.creatTasks, name = 'createTask'),
    path('getTasks/', views.getTasks, name = 'getTasks'),
    path('editTask/<int:task_id>/', views.editTask, name= 'editTask'),
    path('updateTask/', views.updateTask, name= 'updateTask'),
    path('deleteTask/<int:task_id>/', views.deleteTask, name= 'deleteTask'),
    # ex: /polls/5/vote/
]
