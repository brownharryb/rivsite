from django import forms
from django.core.validators import validate_email
import string





class ValidationForm():


	def clean(self):
		for field in self.cleaned_data:
			if isinstance(self.cleaned_data[field], str):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data

	def clean_email_address(self):
		email = self.cleaned_data.get('email_address').strip()
		validate_email(email)
		return email

	def clean_first_name(self):
		return clean_alphabets(self.cleaned_data.get('first_name'))

	def clean_middle_name(self):
		return clean_alphabets(self.cleaned_data.get('middle_name'))

	def clean_last_name(self):
		return clean_alphabets(self.cleaned_data.get('last_name'))

	def clean_date_of_birth(self):
		return self.cleaned_data.get('date_of_birth')

	def clean_phone_number(self):
		return validate_phone(self.cleaned_data.get('phone_number'))

	def clean_phone_number2(self):
		return validate_phone(self.cleaned_data.get('phone_number2'))

	def clean_permanent_residence(self):
		return clean_alphanum(self.cleaned_data.get('permanent_residence'), safe="'()")



def remove_white_spaces(value):
	if value:
		return value.strip().replace("  ","")



def validate_value(value, allowed, validate_empty=True):	
	value = remove_white_spaces(value)
	if validate_empty == False and value in ['',None]:
		return value
	if validate_empty:
		if value in ['', None]:
			raise forms.ValidationError("Value is empty!!")
	for i in value:
		if not i in allowed:
			raise forms.ValidationError("Unallowed character \"{}\" in \"{}\" ".format(i, value))
	return value



def clean_alphabets(value, safe='', validate_empty=False):
	'''Returns only letters.'''
	allowed = string.ascii_letters+safe+'-. '
	return validate_value(value, allowed, validate_empty=validate_empty)

def clean_alphanum(value, safe='', validate_empty=False):
	'''
	Returns a clean value of alphanumeric characters.
	Raises Validation error if not possible.
	'''
	allowed = string.ascii_letters + string.digits + safe+' .-,'	
	return validate_value(value, allowed, validate_empty=validate_empty)

def validate_phone(phone):
	return clean_number(phone, safe='+ ')

def clean_number(value, safe='', validate_empty=False):
	'''Confirm value is a valid number.'''
	allowed = string.digits+safe
	return validate_value(value, allowed, validate_empty=validate_empty)

