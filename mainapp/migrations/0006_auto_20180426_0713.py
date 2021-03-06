# Generated by Django 2.0.4 on 2018-04-26 07:13

from django.db import migrations, models
import mainapp.models.person


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20180425_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='local_govt_id',
            field=models.FileField(null=True, upload_to=mainapp.models.person.user_directory_path),
        ),
        migrations.AddField(
            model_name='candidate',
            name='photo',
            field=models.FileField(null=True, upload_to=mainapp.models.person.user_directory_path),
        ),
    ]
