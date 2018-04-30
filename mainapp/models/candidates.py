from django.db import models
from .person import Person
import random


def generate_pin(length=10):
	pin = ''
	for _ in range(length):
		pin += str(random.randrange(9))
	return pin


def get_file_ext(filename):
	return filename.split(".")[-1]
	

def local_govt_id_file_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	pn = generate_pin(5)
	return 'user_{0}/{1}'.format(instance.user.id, "local_govt_id_{}.{}".format(pn,get_file_ext(filename)))

def photo_file_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	pn = generate_pin(5)
	return 'user_{0}/{1}'.format(instance.user.id, "photo_{}.{}".format(pn,get_file_ext(filename)))


def cv_file_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	pn = generate_pin(5)
	return 'user_{0}/{1}'.format(instance.user.id, "cv_{}.{}".format(pn,get_file_ext(filename)))


class Candidate(Person):
	local_govt_area = models.CharField(max_length=255,null=True)
	height = models.IntegerField(null=True)
	login_key = models.CharField(max_length=20)
	photo = models.FileField(upload_to=photo_file_path)
	local_govt_id = models.FileField(upload_to=local_govt_id_file_path)
	resume = models.FileField(upload_to=cv_file_path, null=True)