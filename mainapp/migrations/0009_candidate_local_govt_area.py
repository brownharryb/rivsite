# Generated by Django 2.0.4 on 2018-04-30 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20180426_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='local_govt_area',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
