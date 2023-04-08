from django.db import models
from django.contrib.auth.models import User


class CaseType(models.Model):
    title = models.CharField(max_length=100, blank=False)
    
    def __str__(self):
        return self.title


# Create your models here.
class EducationalCase(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time_added = models.DateTimeField(auto_now=True)
    case_types = models.ManyToManyField(CaseType, blank=True)
    is_published = models.BooleanField(default=False)
    num_favorited = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
