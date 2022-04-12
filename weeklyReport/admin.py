from django.contrib import admin

# Register your models here.
from .models import Task, Report

admin.site.register(Task)
admin.site.register(Report)