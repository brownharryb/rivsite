from django import forms
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from mainapp.forms.validators import ValidationForm




class LoginForm(ValidationForm, forms.Form):
	form_cat = forms.CharField(widget=forms.HiddenInput(attrs={'value':'login_form'}))
	email_address = forms.CharField(max_length=100, help_text='',label='Email',
		widget=forms.TextInput(attrs={'class':'form-control'}))
	pin = forms.CharField(max_length=100, help_text='',label='Pin',
		widget=forms.PasswordInput(attrs={'class':'form-control'}))


	def page_title(self):
		return "Login"


	def get_form_cat(self):
		return "login_form"

	# def clean_email_address(self):
	# 	email = self.cleaned_data.get('email_address')
	# 	email = ema



