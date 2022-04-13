from django.urls import path

from . import views

app_name = 'announce'
urlpatterns = [
    path('', views.listAnnouncementFiles, name='index'),
    path('upload_announce/', views.upload_announce, name='uploadAnnounce'),
    path('manage_announce/', views.manage_announce, name='manageAnnounce'),
    #path('showAnnounce/<int:report_id>/', views.showReport, name='showReport'),
]