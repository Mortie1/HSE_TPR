from django.urls import path

from .views import *

urlpatterns = [
   path('search/cases_tiles', SearchCasesTilesAjax.as_view(), name="search_cases_tiles"),
   path('search/cases_list', SearchCasesListAjax.as_view(), name="search_cases_list"),
   path('search_user/cases_tiles', SearchUserCasesTilesAjax.as_view(), name="search_user_cases_tiles"),
   path('search_user/cases_list', SearchUserCasesListAjax.as_view(), name="search_user_cases_list"),
]