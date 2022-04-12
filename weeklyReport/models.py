from django.db import models


class Report(models.Model):
    reporter = models.CharField(max_length=30)
    week = models.IntegerField()
    year = models.IntegerField()
    lastUpdateTime = models.DateTimeField(verbose_name='updated Time')
    itemsLastWeek = models.CharField(max_length=30)
    itemsComingWeek = models.CharField(max_length=120)
    others = models.CharField(max_length=120)

    SHIRT_SIZES = (
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

    def __str__(self):
        return self.reporter


class Customer(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    customer_name=models.CharField(max_length=32)
    description = models.CharField(max_length=120)
    ranking = models.IntegerField()
    def __str__(self):
        return self.customer_name


class Task(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    owner = models.CharField(max_length=30)
    week = models.IntegerField()
    year = models.IntegerField()
    createTime = models.DateTimeField(verbose_name='created Time')
    lastUpdateTime = models.DateTimeField(verbose_name='updated Time')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    taskName = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
    progress = models.IntegerField()

    def __str__(self):
        return self.taskName


