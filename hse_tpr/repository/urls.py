from django.urls import path

from .views import *

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('repository/', RepositoryView.as_view(), name='repository'),
    path('repository/create_case/', CreateCaseView.as_view(), name='create_case')
]