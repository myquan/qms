from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('uploadWeeklyReport/', views.uploadWeeklyReport, name='upload'),
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('get_name/', views.get_name, name='getname'),
]
