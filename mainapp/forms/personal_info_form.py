from django import forms
from mainapp.forms.validators import ValidationForm




class PersonalInfoForm(ValidationForm, forms.Form):
	GENDER_CHOICES = (
					("F","Female"),
					("M","Male"),
				)
	form_cat = forms.CharField(widget=forms.HiddenInput(attrs={'value':'personal_info_form'}))
	first_name = forms.CharField(max_length=100, help_text='',label='First Name',
		widget=forms.TextInput(attrs={'class':'form-control'}))
	middle_name = forms.CharField(max_length=100, help_text='',label='Middle Name',
		widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	last_name = forms.CharField(max_length=100, help_text='',label='Last Name',
		widget=forms.TextInput(attrs={'class':'form-control'}))
	gender = forms.ChoiceField(choices=GENDER_CHOICES,label='Gender',
		widget=forms.Select(attrs={'class':'form-control'}))
	date_of_birth = forms.DateField(label='Date Of Birth',
		widget=forms.DateInput(attrs={'class':'form-control datepicker'}))


	def page_title(self):
		return "Personal Information"


	def get_form_cat(self):
		return "personal_info_form"