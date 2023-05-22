from django import template
from django.contrib.auth.models import User
from datetime import date, timedelta
from repository.models import EducationalCase, CaseType

register = template.Library()

@register.simple_tag
def cut_description(description: str) -> str: 
    max_length = 40
    if len(description) > max_length:
        return description[:max_length + 1] + '...'
    else:
        return description