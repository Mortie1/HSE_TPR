from django.contrib import admin

# Register your models here.
from .models import EducationalCase, CaseType, Platform, Faculty, Department, StateSpec, OtherSpec, EducationalLevel

from .models import EducationalCase
# Register your models here.
class EducationalCaseAdmin(admin.ModelAdmin):
    list_filter = ('is_published',)
    list_display = ['case_title', 'is_published']



admin.site.register(CaseType)
admin.site.register(Platform)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(StateSpec)
admin.site.register(OtherSpec)
admin.site.register(EducationalLevel)
admin.site.register(EducationalCase, EducationalCaseAdmin)