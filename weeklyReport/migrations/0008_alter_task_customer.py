# Generated by Django 4.0.3 on 2022-04-10 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weeklyReport', '0007_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weeklyReport.customer'),
        ),
    ]
