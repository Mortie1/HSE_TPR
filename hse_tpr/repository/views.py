from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


import json

from django.views.generic import TemplateView, CreateView, UpdateView
from .forms import EducationalCaseForm
from .models import EducationalCase, CaseType, Platform, Department, StateSpec, OtherSpec, CaseType, EducationalLevel


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'repository/profile.html'


class RepositoryView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'repository/repository.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['models_for_filters'] = {
            'Platform': Platform,
        }
        return context


class CreateCaseView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    form_class = EducationalCaseForm
    template_name = 'repository/create_case.html'

    def form_valid(self, form: EducationalCaseForm) -> HttpResponse:
        user = self.request.user
        case = EducationalCase()
        case = form.save(commit=False)
        case.owner_id = user.pk
        many_to_many_fields = {
            'case_types',
            'educational_levels',
            'state_specs',
            'other_specs',
        }
        case.save()
        for field in many_to_many_fields:
            temp = form.cleaned_data.get(field)
            for item in temp:
                getattr(case, field).add(item)
        case.save()
        return HttpResponseRedirect(reverse_lazy('profile'))


class CaseView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    template_name = 'repository/case.html'
    form_class = EducationalCaseForm

    def get_initial(self):
        initial = super().get_initial()
        case = get_object_or_404(EducationalCase, pk=self.kwargs['case_pk'])
        many_to_many_fields = {
            'case_types',
            'educational_levels',
            'state_specs',
            'other_specs',
        }
        fields = EducationalCase._meta.get_fields()
        for field in fields:
            if field.name in many_to_many_fields:
                initial[field.name] = getattr(case, field.name).all()
            else:
                initial[field.name] = getattr(case, field.name)
        print(initial)
        return initial

        


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = get_object_or_404(EducationalCase, pk=self.kwargs['case_pk'])
        if not case.is_published:
            raise Http404
        if case.is_deleted:
            raise Http404
        context['case'] = case
        return context


class SettingsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'repository/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class CaseUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'repository/update_case.html'
    form_class = EducationalCaseForm
    model = EducationalCase

    def get_initial(self):
        initial = super().get_initial()
        case = get_object_or_404(EducationalCase, pk=self.kwargs['pk'])
        if case.owner != self.request.user or case.is_deleted:
            raise Http404
        many_to_many_fields = {
            'case_types',
            'educational_levels',
            'state_specs',
            'other_specs',
        }
        fields = EducationalCase._meta.get_fields()
        for field in fields:
            if field.name in many_to_many_fields:
                initial[field.name] = getattr(case, field.name).all()
            else:
                initial[field.name] = getattr(case, field.name)
        return initial
    
    
    def form_valid(self, form: EducationalCaseForm) -> HttpResponse:
        user = self.request.user
        case = EducationalCase()
        case = form.save(commit=False)
        case.owner_id = user.pk
        many_to_many_fields = {
            'case_types',
            'educational_levels',
            'state_specs',
            'other_specs',
        }
        case.save()
        for field in many_to_many_fields:
            temp = form.cleaned_data.get(field)
            for item in temp:
                getattr(case, field).add(item)
        case.save()
        return HttpResponseRedirect(reverse_lazy('profile'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = get_object_or_404(EducationalCase, pk=self.kwargs['pk'])
        if case.is_deleted:
            raise Http404
        context['case'] = case
        return context


class SettingsSaveName(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        coming_data = json.loads(request.body)
        response = {}
        try:
            user: User = self.request.user  # type: ignore
            user.first_name = coming_data['first_name']
            user.last_name = coming_data['last_name']
            user.save()
            response = {"OK": 1}
        except:
            response = {"OK": 0}
        return JsonResponse(response)


class SettingsSavePassword(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        coming_data = json.loads(request.body)
        response = {}
        try:
            user: User = self.request.user # type: ignore
            if coming_data['first_password'] != coming_data['second_password']:
                raise ValidationError(
                    ("Пароли не совпадают"),
                    code="passwords_dont_match",
                )
            validate_password(coming_data['first_password'], user=user, )
            user.password = make_password(coming_data['first_password'])
            user.save()
            response = {"OK": 1, "html": ''}
        except ValidationError as e:
            html = '<ul>'
            for message in e.messages:
                html += f"<li>{message}</li>"
            html += '</ul>'
            response = {"OK": 0, "html": html}
        return JsonResponse(response)


class AddNewVariantToSelectField(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request, *args, **kwargs):
        coming_data = json.loads(request.body)
        response = {}
        
        model_to_update = None
        field_name = coming_data['field']
        
        if field_name == 'case_department' or field_name == 'information_author_department':
            model_to_update = Department
        elif field_name == 'case_platform':
            model_to_update = Platform
        elif field_name == 'state_specs':
            model_to_update = StateSpec
        elif field_name == 'other_specs':
            model_to_update = OtherSpec
        elif field_name == 'case_types':
            model_to_update = CaseType
        elif field_name == 'educational_levels':
            model_to_update = EducationalLevel
        
        if model_to_update is None or model_to_update.objects.filter(title=coming_data['input']):
            raise Http404
        
        instance = model_to_update.objects.create(title=coming_data['input'])
        response = {"id": instance.pk}
        return JsonResponse(response)