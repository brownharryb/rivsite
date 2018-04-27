# Generated by Django 2.0.4 on 2018-04-25 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_candidate_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='permanent_residence',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='phone_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='phone_number2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
