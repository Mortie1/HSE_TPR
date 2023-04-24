from django.urls import path

from .views import *

urlpatterns = [
   path('search/cases_tiles', SearchCasesTilesAjax.as_view(), name="search_cases_tiles"),
   path('search/cases_list', SearchCasesListAjax.as_view(), name="search_cases_list"),
   
]