from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'settings'
urlpatterns = [
    path('', views.index, name='index'),
    path('change_password/',
         auth_views.PasswordChangeView.as_view(template_name='registration/passwordChange.html', success_url='/'),
         name='change_password'),

]