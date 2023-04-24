from django.db import models
from django.contrib.auth.models import User


class BasicSimpleModel(models.Model):
    title = models.CharField(max_length=250, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        abstract = True



class CaseType(BasicSimpleModel):
    pass


class Platform(BasicSimpleModel):
    pass
    

class Faculty(BasicSimpleModel):
    pass



class Department(BasicSimpleModel):
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)



class StateSpec(BasicSimpleModel):
    pass


class OtherSpec(BasicSimpleModel):
    pass

class EducationalLevel(BasicSimpleModel):
    pass


# Create your models here.
class EducationalCase(models.Model):
    
    # Auto fields
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time_added = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    num_favorited = models.PositiveIntegerField(default=0)
    
    
    
    # ----- Service Information -----
    
    # Basic case information
    case_title = models.CharField(max_length=250, blank=False)
    case_annotation = models.TextField(blank=True)
    case_platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True, blank=True)
    case_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="case_department", blank=True)
    case_comments = models.TextField(blank=True)
    
    # Information author
    information_author_email = models.EmailField(max_length=250, blank=True)
    information_author_name = models.CharField(max_length=250, blank=True)
    information_author_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="information_author_department", blank=True)
    
    # Case authors
    physical_authors = models.TextField(blank=True)
    entity_author_name = models.CharField(max_length=250, blank=True)
    entity_author_email = models.EmailField(max_length=250, blank=True)
    entity_author_contact = models.CharField(max_length=250, blank=True)
    entity_author_url = models.URLField(max_length=250, blank=True)
    
    # Case usage results
    last_sem_students_num = models.IntegerField(default=0)
    all_time_students_num = models.IntegerField(default=0)
    next_sem_students_num = models.IntegerField(default=0)
    
    # Case usage recommendations
    problems = models.TextField(blank=True)
    what_could_be_improved = models.TextField(blank=True)
    would_you_recommend_in_HSE = models.TextField(blank=True)
    would_you_recommend_in_other_orgs = models.TextField(blank=True)
    paid_unpaid_recommendation = models.TextField(blank=True)
    case_spreading_recommendations = models.TextField(blank=True)
    
    
    
    # ----- Educational Information -----
    
    # Basic information
    case_types = models.ManyToManyField(CaseType, blank=True)
    state_specs = models.ManyToManyField(StateSpec, blank=True)
    other_specs = models.ManyToManyField(OtherSpec, blank=True)
    educational_specialties = models.TextField(blank=True)
    educational_levels = models.ManyToManyField(EducationalLevel, blank=True)
    
    #TODO: tags for easy search

    
    def __str__(self):
        return self.case_title
