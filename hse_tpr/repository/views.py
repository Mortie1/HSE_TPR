from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView, View
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseForbidden

from calendar import monthrange

from datetime import date

import json

from django.views.generic import TemplateView, CreateView, UpdateView
from .forms import EducationalCaseForm
from .models import EducationalCase, CaseType

class ProfileView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'repository/profile.html'
    

class RepositoryView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'repository/repository.html'
    


class CreateCaseView(FormView, LoginRequiredMixin):
    login_url = '/login'
    form_class = EducationalCaseForm
    template_name = 'repository/create_case.html'
    
    def form_valid(self, form) -> HttpResponse:
        user = self.request.user
        case = EducationalCase()
        case = form.save(commit=False)
        case.owner_id = user.pk
        case.save()
        return HttpResponseRedirect(reverse_lazy('repository'))


class CaseView(FormView, LoginRequiredMixin):
    login_url = '/login'
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
                print(field.name, getattr(case, field.name).all())
            else:
                initial[field.name] = getattr(case, field.name)
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