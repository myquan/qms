# Generated by Django 4.0.3 on 2022-04-04 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weeklyReport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='week',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='year',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
