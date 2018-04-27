from django.db import models
from django.contrib.auth.models import User
from datetime import date


def user_directory_path(instance, filename):
	pass


def get_file_ext(filename):
	return filename.split(".")[-1]



def local_govt_id_file_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/{1}'.format(instance.user.id, "local_govt_id.{}".format(get_file_ext(filename)))

def photo_file_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/{1}'.format(instance.user.id, "photo.{}".format(get_file_ext(filename)))

class Person(models.Model):
	SEX_CHOICES = (
			('F','Female'),
			('M','Male'),
		)
	user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
	first_name = models.CharField(max_length=100,null=True)
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100,null=True)
	phone_number = models.CharField(max_length=100,null=True)
	phone_number2 = models.CharField(max_length=100,null=True)
	email_address = models.EmailField()
	permanent_residence = models.TextField(null=True)
	gender = models.CharField(max_length=1, choices=SEX_CHOICES,null=True)
	date_of_birth = models.DateField(null=True)

	@property
	def age(self):
		if self.date_of_birth in ['',None]:
			return "-"
		today = date.today()
		return today.year - self.date_of_birth.year - ((today.month, today.day) < \
							(self.date_of_birth.month, self.date_of_birth.day))
	



	class Meta:
		abstract = True