from django.contrib.auth.mixins import LoginRequiredMixin

from repository.models import CaseType, EducationalCase
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.views.generic import TemplateView
from django.template.loader import render_to_string


class SearchCasesAjax(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    
    def __init__(self, search_template, **kwargs):
        super().__init__(**kwargs)
        self.search_template = search_template
    
    def get(self, *args, **kwargs):
        cases = EducationalCase.objects.filter(
            is_deleted=0, is_published=1,  case_title__icontains=self.request.GET.get('q')).distinct()
        html = render_to_string(
            self.search_template, {'cases': cases})
        return JsonResponse({'html': html})


class SearchCasesTilesAjax(SearchCasesAjax):
    def __init__(self, **kwargs):
        super().__init__("search/search_cases_tiles.html", **kwargs)
    

class SearchCasesListAjax(SearchCasesAjax):
    def __init__(self, **kwargs):
        super().__init__("search/search_cases_list.html", **kwargs)