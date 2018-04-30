from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from mainapp.forms import (PersonalInfoForm, DocumentForm,
							ContactInfoForm, LoginForm)
from mainapp.models import Candidate
import random
import logging

logger = logging.getLogger(__name__)


def generate_pin(length=10):
	pin = ''
	for _ in range(length):
		pin += str(random.randrange(9))
	return pin


def logout_user(request):
	logout(request)
	return redirect("/")

def get_login_pin(user):
	candidate = Candidate.objects.filter(user=user)[0]
	return candidate.login_key




class ApplicationFormView(View):

	template = "home.html"
	personal_form_class = PersonalInfoForm
	document_form_class = DocumentForm
	contact_form_class = ContactInfoForm
	login_form_class = LoginForm


	def get(self, request, *args, **kwargs):
		if request.path == reverse("apply_new_page"):
			form = self.contact_form_class()
			html = render_to_string('form_template.html',{'form_html':form},
						request=request)
			return HttpResponse(html)
		if not request.user.is_authenticated:
			form = self.login_form_class()
			if request.is_ajax():
				html = render_to_string('form_template.html',{'form_html':form},
						request=request)
				return HttpResponse(html)
			return render(request, self.template, {'form_html':form})
		else:
			form = self.get_filled_contact_form(request.user)
			if request.is_ajax():
				html = render_to_string('form_template.html',{'form_html':form},
						request=request)
				return HttpResponse(html)
			return render(request, self.template, {'form_html':form})
			

	def post(self, request, *args, **kwargs):
		form_name = request.POST.get('form_cat')
		if not form_name:
			raise Http404()
		if form_name == 'login_form':
			form = self.login_form_class(request.POST)
			if form.is_valid():
				username = form.cleaned_data['email_address']
				password = form.cleaned_data['pin']
				user = authenticate(request, username=username, password=password)
				if user is not None:
					login(request,user)
					form = self.get_filled_contact_form(user)
					if request.is_ajax():
						html = render_to_string('form_template.html',{'form_html':form},
								request=request)
						return HttpResponse(html)
					return render(request, self.template, {'form_html':form})
				else:
					form.add_error(None,"Invalid Username or Pin!!")
					if request.is_ajax():
						html = render_to_string('form_template.html',{'form_html':form},
								request=request)
						return HttpResponse(html)
					return render(request, self.template, {'form_html':form})
			else: #form is not valid
				if request.is_ajax():
					html = render_to_string('form_template.html',{'form_html':form},
							request=request)
					return HttpResponse(html)
				return render(request, self.template, {'form_html':form})

		if form_name == "contact_form":
			form = self.contact_form_class(request.POST)
			if form.is_valid():
				if not request.user.is_authenticated:
					email = form.cleaned_data['email_address']
					if User.objects.filter(username=email).exists():
						form.add_error(None,"User already exists!")
						if request.is_ajax():
							html = render_to_string('form_template.html',{'form_html':form},
									request=request)
							return HttpResponse(html)
						return render(request, self.template, {'form_html':form})
					user = self.try_to_create_user(request,form)
					self.save_contact_form_information(user,request.POST)
					form = self.personal_form_class()
					if request.is_ajax():
						html = render_to_string('form_template.html',{'form_html':form},
								request=request)
						return HttpResponse(html)
					return render(request, self.template, {'form_html':form})
				else:
					self.save_contact_form_information(request.user,request.POST)
					form = self.get_filled_personal_class_form(request.user)
					if request.is_ajax():
						html = render_to_string('form_template.html',{'form_html':form},
								request=request)
						return HttpResponse(html)
					return render(request, self.template, {'form_html':form})
			else:
				if request.is_ajax():
					html = render_to_string('form_template.html',{'form_html':form},
							request=request)
					return HttpResponse(html)
				return render(request, self.template, {'form_html':form})
		if form_name == "personal_info_form":
			form = self.personal_form_class(request.POST)
			if form.is_valid():
				if not request.user.is_authenticated:
					return self.login_form_class()
				self.save_personal_form_information(request.user,request.POST)
				form = self.get_filled_document_form(request.user)
				if request.is_ajax():
					html = render_to_string('form_template.html',{'form_html':form},
							request=request)
					return HttpResponse(html)
				return render(request, self.template, {'form_html':form})
			else:
				if request.is_ajax():
					html = render_to_string('form_template.html',{'form_html':form},
							request=request)
					return HttpResponse(html)
				return render(request, self.template, {'form_html':form})

		if form_name == "documents_form":
			form = self.document_form_class(request.POST, request.FILES)
			if form.is_valid():
				if not request.user.is_authenticated:
					return self.login_form_class()
				fields = self.save_documents_form_info(request)
				if fields:
					form = self.get_filled_document_form(request.user)
					for field in fields:
						form.add_error(field,"File is missing!")
					if request.is_ajax():
						html = render_to_string('form_template.html',{'form_html':form},
								request=request)
						return HttpResponse(html)
					return render(request, self.template, {'form_html':form})
				if request.is_ajax():
					html = render_to_string('success_page.html',{'pin':get_login_pin(request.user)},
							request=request)
					return HttpResponse(html)
				return render(request, self.template, {'form_html':form})
				
			else:
				form = self.get_filled_document_form(request.user)
				if request.is_ajax():
					html = render_to_string('form_template.html',{'form_html':form},
							request=request)
					return HttpResponse(html)
				return render(request, self.template, {'form_html':form})

		# is_not = self.check_authentic_user(request)
		# if is_not:
		# 	return is_not

	def try_to_create_user(self,request,cleaned_contact_form):
		email = cleaned_contact_form.cleaned_data['email_address']
		password = generate_pin()
		user = User.objects.create_user(username=email,email=email,password=password)
		candidate = Candidate.objects.create(user=user)
		candidate.login_key = password
		candidate.save()
		self.send_user_an_email_with_pin(email,password)
		login(request,user)
		return user

	def send_user_an_email_with_pin(self, username, password):
		try:
			msg = "Hi someone registered you on .... with your email, your pin is {}".format(password)
			success = send_mail("New Application",msg,settings.DEFAULT_FROM_EMAIL,[username])
		except Exception as e:
			logger.debug(e)


	def get_filled_personal_class_form(self,user):
		candidate = Candidate.objects.filter(user=user)
		if not candidate:
			return self.personal_form_class()
		candidate = candidate[0]
		data = {"first_name":candidate.first_name,
				"middle_name":candidate.middle_name,
				"last_name":candidate.last_name,
				"gender":candidate.gender,
				"local_govt_area":candidate.local_govt_area,
				"date_of_birth":candidate.date_of_birth}
		return self.personal_form_class(data)



	def get_filled_contact_form(self,user):
		candidate = Candidate.objects.filter(user=user)
		if not candidate:
			return self.contact_form_class()
		candidate = candidate[0]
		data = {"phone_number":candidate.phone_number,
				"phone_number2":candidate.phone_number2,
				"email_address":candidate.email_address,
				"permanent_residence":candidate.permanent_residence}
		return self.contact_form_class(data)

	def get_filled_document_form(self,user):
		candidate = Candidate.objects.filter(user=user)
		if not candidate:
			return self.document_form_class()
		candidate = candidate[0]
		data = {'local_govt_id':candidate.local_govt_id or None,
				'photo':candidate.photo or None,
				'resume':candidate.resume or None
				}
		form = self.document_form_class(files=data)
		return form

	def save_contact_form_information(self, user, request_post_data):
		candidate = Candidate.objects.get_or_create(user=user)[0]
		candidate.email_address = user.email
		candidate.permanent_residence = request_post_data.get('permanent_residence')
		candidate.phone_number=request_post_data.get('phone_number')
		candidate.phone_number2=request_post_data.get('phone_number2')
		candidate.save()

	def save_personal_form_information(self,user, request_post_data):
		candidate = Candidate.objects.get_or_create(user=user)[0]
		candidate.first_name = request_post_data.get('first_name')
		candidate.middle_name = request_post_data.get('middle_name')
		candidate.last_name=request_post_data.get('last_name')
		candidate.date_of_birth=request_post_data.get('date_of_birth')
		candidate.local_govt_area=request_post_data.get('local_govt_area')
		candidate.gender=request_post_data.get('gender')
		candidate.save()

	def save_documents_form_info(self,request):
		candidate = Candidate.objects.get_or_create(user=request.user)[0]
		if request.FILES.get('photo') not in ['',None]:
			candidate.photo = request.FILES.get('photo')
		if request.FILES.get('local_govt_id') not in ['',None]:
			candidate.local_govt_id = request.FILES.get('local_govt_id')
		if request.FILES.get('resume') not in ['',None]:
			candidate.resume = request.FILES.get('resume')
		candidate.save()
		candidate.refresh_from_db()
		err = []
		for field in ['local_govt_id','photo','resume']:
			if getattr(candidate,field) in ['',None]:
				err.append(field)
		return err



	def check_authentic_user(self, request):
		if not request.user.is_authenticated:
			form = self.login_form_class()
			if request.is_ajax():
				html = render_to_string('form_template.html',{'form_html':form},
						request=request)
				return HttpResponse(html)
			return render(request, self.template, {'form_html':form})





















			
	# 	personal_form = self.personal_form_class()
	# 	document_form = self.document_form_class()
	# 	contact_form = self.contact_form_class()
	# 	return render(request, self.template, {'form_html':self.get_next_form(request)})

	# def post(self, request, *args, **kwargs):
	# 	form_name = request.POST.get('form_cat')
	# 	if not form_name:
	# 		raise Http404()
	# 	if form_name == "login_form":
	# 		form =  self.process_login_form(request)
	# 	if form_name == "contact_form":
	# 		form =  self.process_contact_form(request)
	# 	elif form_name == "personal_form":
	# 		form =  self.process_personal_form()
	# 	elif form_name == "document_form":
	# 		form =  self.process_document_form()

	# 	if request.is_ajax():
	# 		html = render_to_string('form_template.html',{'form_html':form},
	# 			request=request)
	# 		return HttpResponse(html)
	# 	return render(request, self.template, {'form_html':form})

		

	# def process_contact_form(self, request):
	# 	if not request.POST:
	# 		return self.contact_form_class()
	# 	contact_form = self.contact_form_class(request.POST)
	# 	if contact_form.is_valid():
	# 		return self.process_personal_form(request)
	# 	return contact_form

	# def process_login_form(self, request):
	# 	if not request.POST:
	# 		login_form = self.login_form_class()
	# 		return login_form
	# 	login_form = self.login_form_class(request.POST)
	# 	if login_form.is_valid():
	# 		return self.process_contact_form(request)
	# 	return login_form
		


	# def process_personal_form(self,request):
	# 	if not request.POST:
	# 		return self.personal_form_class()
	# 	personal_form = self.contact_form_class(request.POST)
	# 	if personal_form.is_valid():
	# 		return self.process_document_form(request)
	# 	return personal_form

	# def process_document_form(self,request):
	# 	if not request.POST:
	# 		return self.document_form_class()
	# 	document_form = self.document_form_class(request.POST)
		

	# def get_next_form(self,request):
	# 	if not request.user.is_authenticated:
	# 		return self.process_login_form(request)			
	# 	return HttpResponse("ok")