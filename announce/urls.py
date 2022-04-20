from django.urls import path

from . import views

app_name = 'announce'
urlpatterns = [
    path('', views.manage_announcements, name='index'),
    path('upload_announce/', views.upload_announce, name='uploadAnnouncement'),
    path('update_announce/', views.update_announce, name='updateAnnouncement'),
    path('manage_announce/', views.manage_announcements, name='manageAnnounce'),
    path('delete_announce/<int:announce_id>/', views.delete_announcements, name='deleteAnnounce'),
    path('edit_announce/<int:announce_id>/', views.edit_announcements, name='editAnnounce'),
    path('get_announce/<int:category_id>/', views.get_announcements, name='getAnnounce'),
    path('get_clockin_list/',views.clock_in_list, name='getClockinList'),
    path('test/', views.index, name='test'),
]