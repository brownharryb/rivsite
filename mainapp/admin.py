from django.contrib import admin
from .models import *



@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","phone_number",
    			"email_address","height","gender","age","photo")
    list_filter = ("gender","height","local_govt_area")