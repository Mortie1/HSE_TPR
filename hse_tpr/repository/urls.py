from django.urls import path

from .views import *

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('repository/', RepositoryView.as_view(), name='repository'),
    path('repository/create_case/', CreateCaseView.as_view(), name='create_case'),
    path('repository/<int:case_pk>/', CaseView.as_view(), name='case'),
    path('profile/settings/', SettingsView.as_view(), name='settings'),
    path('repository/case_update/<int:pk>/', CaseUpdateView.as_view(), name='case_update'),
    path('profile/settings/save_password/', SettingsSavePassword.as_view(), name='save_password'),
    path('profile/settings/save_name/', SettingsSaveName.as_view(), name='save_name'),
    path('add_my_variant/', AddNewVariantToSelectField.as_view(), name="add_my_variant"),
]