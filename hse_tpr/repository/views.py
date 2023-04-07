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
# from .forms import ExerciseForm, TrainingForm, TagForm
# from .models import Exercises, Trainings, ExcerciseMarkers

class ProfileView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'repository/profile.html'