from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm

from .models import EducationalCase, CaseType

from django.utils.translation import gettext_lazy as _

class EducationalCaseForm(forms.ModelForm):
    
    class Meta:
        model = EducationalCase
        fields = ['title', 'description', 'case_types']
        CASE_TYPE_OPTIONS = CaseType.objects.all()
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control", "placeholder":"Введите название кейса",}),
            'description': forms.Textarea(attrs={'class':"form-control", "rows": "4", "cols": "135", "placeholder": "Описание кейса", "maxlength": "150",}),
            'case_types': forms.SelectMultiple(choices=CASE_TYPE_OPTIONS)
        }
    
    
    def clean_title(self):
        title = self.cleaned_data['title']
        cases = EducationalCase.objects.filter(title__iexact=title)
        if cases.exists():
            raise ValidationError("Кейс с таким названием уже существует")
        return title
    
    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_case_types(self):
        case_types = self.cleaned_data['case_types']
        return case_types
