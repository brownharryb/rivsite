# Generated by Django 2.0.4 on 2018-04-24 19:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2018, 4, 24, 19, 43, 25, 278775, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='candidate',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
