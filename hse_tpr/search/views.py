from django.contrib.auth.mixins import LoginRequiredMixin

from repository.models import EducationalCase
from django.http import JsonResponse

from django.views.generic import View
from django.template.loader import render_to_string


class SearchCasesAjax(LoginRequiredMixin, View):
    login_url = '/login'
    
    def __init__(self, search_template, **kwargs):
        super().__init__(**kwargs)
        self.search_template = search_template
    
    def get(self, *args, **kwargs):
        request_vars = self.request.GET
        filters_names = request_vars.keys()
        cases = EducationalCase.objects.filter(
            is_deleted=0,  case_title__icontains=self.request.GET.get('q')).distinct()
        is_profile = False
        for key in filters_names:
            if key == 'q':
                continue
            if request_vars[key] != "None":
                if key == 'Platform':
                    cases = cases.filter(case_platform__in=list(map(int, request_vars[key]))).distinct()
                elif key == 'information_author_name':
                    cases = cases.filter(information_author_name__icontains=request_vars[key]).distinct()
                elif key == 'profile' and request_vars[key] == '1':
                    cases = cases.filter(owner_id=self.request.user.pk).distinct()
                    is_profile = True
        if not is_profile:
            cases = cases.filter(is_published=1)
        html = render_to_string(
            self.search_template, {'cases': cases})
        return JsonResponse({'html': html})


class SearchUserCasesTilesAjax(SearchCasesAjax):
    def __init__(self, **kwargs):
        super().__init__("search/search_cases_tiles.html", **kwargs)
        
    def get(self, *args, **kwargs):
        
        cases = EducationalCase.objects.filter(
            is_deleted=0, case_title__icontains=self.request.GET.get('q'), owner_id=self.request.user.pk).distinct()
        html = render_to_string(
            self.search_template, {'cases': cases})
        return JsonResponse({'html': html})


class SearchUserCasesListAjax(SearchCasesAjax):
    def __init__(self, **kwargs):
        super().__init__("search/search_cases_list.html", **kwargs)
        
    def get(self, *args, **kwargs):
        cases = EducationalCase.objects.filter(
            is_deleted=0, case_title__icontains=self.request.GET.get('q'), owner_id=self.request.user.pk).distinct()
        html = render_to_string(
            self.search_template, {'cases': cases})
        return JsonResponse({'html': html})


class SearchCasesTilesAjax(SearchCasesAjax):
    def __init__(self, **kwargs):
        super().__init__("search/search_cases_tiles.html", **kwargs)
    

class SearchCasesListAjax(SearchCasesAjax):
    def __init__(self, **kwargs):
        super().__init__("search/search_cases_list.html", **kwargs)