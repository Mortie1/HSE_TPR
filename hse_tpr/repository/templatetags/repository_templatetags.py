from django import template
from django.contrib.auth.models import User
from datetime import date, timedelta
from repository.models import EducationalCase, CaseType

register = template.Library()

@register.filter
def is_multiple_choice(field): 
    select_fields = {
        "case_types",
        "state_specs",
        "other_specs",
        "educational_levels"
    }
    if field.name in select_fields:
        return True
    return False



@register.simple_tag
def edit_if_select(field, case):
    select_fields = {
        "case_types",
        "case_platform",
        "case_department",
        "information_author_department",
        "state_specs",
        "other_specs",
        "educational_levels"
    }
    if field.name not in select_fields:
        return field
    choices = []
    # try:
    if getattr(case, field.name) == None:
        choices = [(None, "Не выбрано")]
        field.choices = choices
        return field
    for value in getattr(case, field.name).all():
        print('xxx')
        choices.append((None, value.title))
    # except:
    #     choices = [(None, getattr(case, field.name))]
    field.choices = choices
    print(field.choices)
    return field