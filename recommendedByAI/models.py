from django.db import models
from common.utils.chooseConstant import STATUS_CHOICES
from common.utils.text import unique_slug
from employee.models import EmployeePreferences
from employer.models import JobRequisition
from jobDoggApp import settings

#RecommendedJobs
class RecommendedJobs(models.Model):
    employee_preferences = models.ForeignKey(EmployeePreferences, on_delete=models.CASCADE)
    job_requisition = models.ForeignKey(JobRequisition, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def user(self):
        return self.employee_preferences.user

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.employee_preferences.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_preferences.user.username}"
    
class AppliedJobHistory(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(RecommendedJobs, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    message = models.TextField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.job}"