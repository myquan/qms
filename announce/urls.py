from django.urls import path

from . import views

app_name = 'announce'
urlpatterns = [
    path('', views.listAnnouncementFiles, name='index'),
    path('upload_announce/', views.upload_announce, name='uploadAnnouncement'),
    path('manage_announce/', views.manage_announcements, name='manageAnnounce'),
    path('delete_announce/<int:announce_id>/', views.delete_announcements, name='deleteAnnounce'),
    path('edit_announce/<int:announce_id>/', views.edit_announcements, name='editAnnounce'),
    #path('showAnnounce/<int:report_id>/', views.showReport, name='showReport'),
]