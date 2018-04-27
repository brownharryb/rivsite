from django import forms
from mainapp.forms.validators import ValidationForm



class ContactInfoForm(ValidationForm, forms.Form):
	form_cat = forms.CharField(widget=forms.HiddenInput(attrs={'value':'contact_form'}))
	phone_number = forms.CharField(max_length=100, help_text='Ex: +2348012345678 or 08012345678',label='Mobile',
		widget=forms.TextInput(attrs={'class':'form-control'}))
	phone_number2 = forms.CharField(max_length=100, help_text='',label='Mobile2',
		widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	email_address = forms.CharField(max_length=100, help_text='',label='Email',
		widget=forms.EmailInput(attrs={'class':'form-control'}))
	permanent_residence = forms.CharField(label='Residence',
		widget=forms.Textarea(attrs={'class':'form-control'}),required=False)



	def page_title(self):
		return "Contact Information"


	def get_form_cat(self):
		return "contact_form"