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
        case = EducationalCase()
        case.title = form.clean_title()
        case.description = form.clean_description()
        case.owner_id = self.request.user.pk
        case.save()
        for case_type in form.clean_case_types():
            case.case_types.add(case_type)
        case.save()
        return HttpResponseRedirect(reverse_lazy('repository'))