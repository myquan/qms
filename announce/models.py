from django.db import models


# Create your models here.
class Category_Announcement(models.Model):
    category_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    description = models.CharField(max_length=120)

    def __str__(self):
        return self.category_name


class Announcement(models.Model):
    announce_name = models.CharField(max_length=30)
    file_name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    description = models.CharField(max_length=120, verbose_name='說明')
    category = models.ForeignKey(Category_Announcement, on_delete=models.CASCADE)
    uploader = models.CharField(max_length=20)

    def __str__(self):
        return self.file_name


class ClockRecord(models.Model):
    account_name = models.CharField(max_length=24)
    create_time = models.DateTimeField(auto_now_add=True)

