from django import forms
from mainapp.models import Candidate
from mainapp.forms.custom_fields import RestrictedFileField
from mainapp.forms.validators import ValidationForm




class DocumentForm(ValidationForm, forms.Form):
	form_cat = forms.CharField(widget=forms.HiddenInput(attrs={'value':'documents_form'}))
	photo = RestrictedFileField(content_types=['image/jpeg','image/png'],
		label='Passport Photograph',
		widget=forms.FileInput(attrs={'class':'form-control'}),required=False)
	local_govt_id = RestrictedFileField(content_types=['image/jpeg','image/png'],
		label='Local Govt. Identification',
		widget=forms.FileInput(attrs={'class':'form-control'}), required=False)

	def page_title(self):
		return "Relevant Documents"

	def get_form_cat(self):
		return "documents_form"