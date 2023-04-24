from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.db.models.functions import Lower 

from .models import EducationalCase, CaseType, Platform, Faculty, Department, StateSpec, OtherSpec, EducationalLevel

from django.utils.translation import gettext_lazy as _

class EducationalCaseForm(forms.ModelForm):
    error_css_class = "error"
    
    class Meta:
        model = EducationalCase
        fields = [
            'case_title',
            'case_annotation',
            'case_platform',
            'case_department',
            'case_comments',
            'information_author_email',
            'information_author_name',
            'information_author_department',
            'physical_authors',
            'entity_author_name',
            'entity_author_email',
            'entity_author_contact',
            'entity_author_url',
            'last_sem_students_num',
            'all_time_students_num',
            'next_sem_students_num',
            'problems',
            'what_could_be_improved',
            'would_you_recommend_in_HSE',
            'would_you_recommend_in_other_orgs',
            'paid_unpaid_recommendation',
            'case_spreading_recommendations',
            'case_types',
            'state_specs',
            'other_specs',
            # 'educational_specialties',
            'educational_levels'
        ]
        
        def gettitle(instance):
            return instance.title
        
        def get_sorted_by_title(model):
            objs = model.objects.all()
            res = []
            for obj in objs:
                res.append((obj.pk, obj.title))
            res.sort(key=lambda x: x[1])
            print(res)
            return res
        
                
        # CASE_TYPE_OPTIONS = list(CaseType.objects.order_by('title'))
        # CASE_PLATFROM_OPTIONS = sorted(list(Platform.objects.all()), key=lambda x: x.title)
        # CASE_DEPARTMENT_OPTIONS = get_sorted_by_title(Department)
        # STATE_SPECS_OPTIONS =  sorted(list(StateSpec.objects.all()), key=lambda x: x.title)
        # OTHER_SPECS_OPTIONS = sorted(list(OtherSpec.objects.all()), key=lambda x: x.title)
        # ED_LVLS_OPTIONS = sorted(list(EducationalLevel.objects.order_by('title')), key=lambda x: x.title)
        widgets = {
            'case_title': forms.TextInput(attrs={
                'class': "form-control",
                "placeholder":"Введите название кейса",
            }),
            'case_annotation': forms.Textarea(attrs={'class':"form-control", "rows": "4", "cols": "135", "placeholder": "Краткое описание кейса, его применения",}),
            'case_types': forms.SelectMultiple(attrs={'class': "form-select", 'label': 'Выберите тип кейса'}),
            'case_platform': forms.Select(attrs={'class': "form-select", 'label': 'Выберите платформу'}),
            'case_department': forms.Select(attrs={'class': "form-select", 'aria-label': 'Выберите департамент'}),
            'case_comments': forms.Textarea(attrs={
                'class': "form-control",
                'rows': "4",
                'cols': "135",
                'placeholder': "Введите существенную информацию о кейсе",
            }),
            'information_author_email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': "Введите email автора информации",
            }),
            'information_author_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Введите имя автора информации",
            }),
            'information_author_department': forms.Select(attrs={
                'class': "form-select",
                'aria-label': 'Выберите департамент автора информации',
            }),
            'physical_authors': forms.Textarea(attrs={
                'class': "form-control",
                "rows": "4",
                "cols": "135",
                'placeholder': "Введите имя/имена автор(ов) кейса в следующем формате: ФИО - контактный номер - email - место работы",
            }),
            'entity_author_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Введите название юридического лица-автора кейса",
            }),
            'entity_author_email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': "Введите email юридического лица-автора кейса",
            }),
            'entity_author_contact': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Введите телефон юридического лица-автора кейса",
            }),
            'entity_author_url': forms.URLInput(attrs={
                'class': "form-control",
                'placeholder': "Введите URL сайта юридического лица-автора кейса",
            }),
            'last_sem_students_num': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': "Введите количество студентов прошлого семестра",
            }),
            'all_time_students_num': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': "Введите общее количество студентов",
            }),
            'next_sem_students_num': forms.NumberInput(attrs={'class':"form-control", "placeholder":"Введите ожидаемое количество студентов, которые будут использовать кейс в следующем семестре"}),
            'problems': forms.Textarea(attrs={'class':"form-control", "rows": "4", "cols": "135", "placeholder": "Опишите проблемы и недостатки в использовании кейса",}),
            'what_could_be_improved': forms.Textarea(attrs={'class':"form-control", "rows": "4", "cols": "135", "placeholder": "Что можно улучшить в этом кейсе?",}),
            'would_you_recommend_in_HSE': forms.Textarea(attrs={'class':"form-control", "rows": "4", "cols": "135", "placeholder": "Рекомендовали бы вы использовать данный кейс в ВШЭ?",}),
            'would_you_recommend_in_other_orgs': forms.Textarea(attrs={'class':"form-control", "rows": "4", "cols": "135", "placeholder": "Рекомендовали бы вы использовать данный кейс в других организациях?", }),
            'paid_unpaid_recommendation': forms.Textarea(attrs={'class':"form-control", "rows": "4", "cols": "135", "placeholder": "Как бы вы рекомендовали использовать данный кейс? (платно / бесплатно)",}),
            'case_spreading_recommendations': forms.Textarea(attrs={'class':"form-control", "rows": "4", "cols": "135", "placeholder": "Предложения по условиям распространения кейса",}),
            'state_specs': forms.SelectMultiple(attrs={'class': "form-select",}),
            'other_specs': forms.SelectMultiple(attrs={'class': "form-select", 'aria-label': 'Предметная область (общее)'}),
            # 'educational_specialties': forms.SelectMultiple(choices=ED_SPECS_OPTIONS, attrs={'class': "form-select", 'aria-label': 'Специальности обучения'}),
            'educational_levels': forms.SelectMultiple(attrs={'class': "form-select", 'aria-label': 'Уровень обучения'}),
        }
        labels = {
            'case_title': "Название кейса",
            'case_annotation': "Аннотация кейса",
            'case_types': "Тип кейса",
            
            'case_platform': "Платформа/сервис/ ПО – наименование программного обеспечения, используемого для работы кейса",
            'case_department': "Департамент, ответственный за кейс",
            'case_comments': "Cущественная информация о кейсе",
            'information_author_email': "Email автора введенной в репозиторий информации о кейсе",
            'information_author_name': "Имя автора введенной в репозиторий информации о кейсе",
            'information_author_department': "Департамент автора введенной в репозиторий информации о кейсе",
            'physical_authors': "Автор(ы) кейса",
            'entity_author_name': "Юридическое лицо-автор кейса",
            'entity_author_email': "Email юридического лица-автора кейса",
            'entity_author_contact': "Телефон юридического лица-автора кейса",
            'entity_author_url': "Веб-сайт юридического лица-автора кейса",
            'last_sem_students_num': "Кол-во студентов, обученных в закончившемся семестре",
            'all_time_students_num': "Кол-во студентов, обученных за все время использования кейса",
            'next_sem_students_num': "Кол-во студентов, которое планируется обучить в текущем (будущем) семестре",
            'problems': "Проблемы и недостатки в использовании кейса ",
            'what_could_be_improved': "Что можно улучшить в содержании и применении кейса?",
            'would_you_recommend_in_HSE': "Предложили бы вы использовать данный кейс коллегам в НИУ ВШЭ? ",
            'would_you_recommend_in_other_orgs': "Предложили бы вы использовать данный кейс коллегам в сторонних организациях?",
            'paid_unpaid_recommendation': "Как бы вы рекомендовали использовать данный кейс? (платно / бесплатно)",
            'case_spreading_recommendations': "Предложения по условиям распространения кейса ",
            'state_specs': "Предметная область (гос. классификация)",
            'other_specs': "Предметная область (другое)",
            # 'educational_specialties',
            'educational_levels': "Уровень обучения"
            
        }
    
    
    def __init__(self, *args, **kwargs):
        super(EducationalCaseForm, self).__init__(*args, **kwargs)
        
        def get_choices(model, is_single=False):
            objs = model.objects.all()
            res = []
            for obj in objs:
                res.append((obj.pk, obj.title))
            res.sort(key=lambda x: x[1])
            x = []
            if is_single:
                x = [(None, "Не выбрано")]
            x.extend(res)
            return x
        
        self.fields['case_department'].choices = get_choices(Department, is_single=True)
        self.fields['case_types'].choices = get_choices(CaseType)
        self.fields['case_platform'].choices =get_choices(Platform, is_single=True)
        self.fields['information_author_department'].choices = get_choices(Department, is_single=True)
        self.fields['state_specs'].choices = get_choices(StateSpec)
        self.fields['other_specs'].choices = get_choices(OtherSpec)
        self.fields['educational_levels'].choices = get_choices(EducationalLevel)
    
    # def clean_title(self):
    #     title = self.cleaned_data['case_title']
    #     cases = EducationalCase.objects.filter(title__iexact=title, is_deleted=0)
    #     if cases.exists():
    #         raise ValidationError("Кейс с таким названием уже существует")
    #     return title
    
    # def clean_description(self):
    #     description = self.cleaned_data['case_annotation']
    #     return description

    # def clean_case_types(self):
    #     case_types = self.cleaned_data['case_types']
    #     return case_types
