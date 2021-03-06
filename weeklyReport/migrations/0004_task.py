# Generated by Django 4.0.3 on 2022-04-09 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weeklyReport', '0003_report_others'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=30)),
                ('week', models.IntegerField()),
                ('year', models.IntegerField()),
                ('createTime', models.DateTimeField(verbose_name='created Time')),
                ('lastUpdateTime', models.DateTimeField(verbose_name='updated Time')),
                ('taskName', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=120)),
                ('progress', models.IntegerField()),
            ],
        ),
    ]
