"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from mysite import views

urlpatterns = [
    path('', views.Hello, name='hello'),
    path('polls/', include('polls.urls')),
    path('no-rush/', views.norush),
    path('faqs/', views.faqs),
    path('weeklyReport/', include('weeklyReport.urls')),
    path('settings/', include('settings.urls')),
    path('announce/', include('announce.urls')),
    path('admin/', admin.site.urls),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
