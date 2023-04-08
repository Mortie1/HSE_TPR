from django.contrib import admin

# Register your models here.
from .models import CaseType, EducationalCase
admin.site.register(CaseType)
admin.site.register(EducationalCase)