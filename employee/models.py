import re
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from common.utils.text import unique_slug
from localflavor.us.models import USStateField 
from localflavor.us.us_states import STATE_CHOICES
from common.utils.chooseConstant import (
    DISCHARGE_YEAR_CHOICES, 
    DUTY_FLAG_CHOICES,
    BRANCH, RANK_CHOICES, 
    SCHOOL_TYPE_CHOICES,
    DEGREE_TYPE_CHOICES,
    SALARY_TYPES,
    JOB_TYPES,
    RELOCATION,
    TEST_STATES,
    )
from multiupload.fields import MultiFileField 


#Profile Safety_Video_and_Test, PROFILE DETAILS(Profile Photo ,Tell us all the interesting things about you, 
# UPLOAD YOUR VIDEO(Supported Video Formats: mp4, mpg, avi, mov, mkv, wmv, ogv, webm, flv You can upload a video, however if it is longer than 2 minutes, it will be cut to 2 minutes.  Record Video or uploading)),
# Background_Check, Treat_Box,  Select Ride
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_created = models.BooleanField(default=False)
    companyPolices_completed = models.BooleanField(default=False)
    basic_information_completed = models.BooleanField(default=False)
    personal_information_completed = models.BooleanField(default=False)
    Military_completed = models.BooleanField(default=False)
    Education_completed = models.BooleanField(default=False)
    Experience_completed = models.BooleanField(default=False)
    Preferences_completed = models.BooleanField(default=False)
    
    SkillSetTest_completed = models.BooleanField(default=False)
    OnProgressSkillTest_completed = models.BooleanField(default=False)
    Skipped_completed = models.BooleanField(default=False)
    
    Safety_Video_and_Test_completed = models.BooleanField(default=False)
    VideoResume_completed = models.BooleanField(default=False)
    ResumeUploading_completed = models.BooleanField(default=False)
    
    #Background_Check_completed = models.BooleanField(default=False)
    #Treat_Box_completed = models.BooleanField(default=False)
    #Select_Ride_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)
           
#Policies
class Policies(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title

#UserAcceptedPolicies  
class UserAcceptedPolicies(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    policies = models.ForeignKey(Policies, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, editable=False)

    def __str__(self):
        return str(f'{self.policies}-{self.accepted}')

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
        
#BASIC INFORMATION MODELS   
class BasicInformation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    apartment = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state =  USStateField()
    zip_code = models.CharField(max_length=10)
    cell_phone = models.CharField(max_length=20)
    home_phone = models.CharField(max_length=20)
    work_phone = models.CharField(max_length=20)
    email = models.EmailField()
    emergency_contact_number = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} {self.zip_code}"
    
#Language models 
class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

#SocialSecurityNumberField
class SocialSecurityNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)  # Assuming no dashes or separators
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        if not validate_social_security_number(value):
            raise ValidationError('Invalid social security number.')

def validate_social_security_number(ssn):
    
    # Check for the valid format: XXX-XX-XXXX 
    ssn_validate_pattern = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$"
    
    p = re.compile(ssn_validate_pattern) 
    if (ssn == None):
        return False
    else:
        if(re.search(p, ssn)):
            return True
        else:
            return False
    # Additional validation rules can be added here based on specific requirements
    return True

#PERSONAL INFORMATION MODELS 
class Personal(models.Model):
    GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),('O', 'Other'),)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    social_security_number = SocialSecurityNumberField()
    drivers_license_number = models.CharField(max_length=20)
    drivers_license_state = USStateField()
    date_of_birth = models.DateField(verbose_name= "Date of Birth", null=True , blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    languages = models.ManyToManyField('Language')
    e_verify = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.nickname} {self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nickname} ({self.user.username})"
    
#Military
class Military(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    branch = models.CharField(max_length=50, choices=BRANCH)
    rank = models.CharField(max_length=100, choices=RANK_CHOICES)
    discharge_year = models.DateField(verbose_name="discharge year" )
    duty_flag = models.CharField(max_length=50, choices=DUTY_FLAG_CHOICES) 
    certification_license = models.FileField(upload_to='certificationsMilitary/')
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def form_valid(self, form):
        military = form.save(commit=False)
        military.user = self.request.user
        military.save()
        
        # Update the profile completion status
        profile = get_object_or_404(Profile, user=self.request.user)
        profile.Military_completed = True
        profile.save()

        return super().form_valid(form)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.branch} {self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
           
    def __str__(self):
        return f"{self.user.username}'s Military Information"
    
class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES)
    school_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    graduated = models.BooleanField(default=False)
    graduation_date = models.DateField(null=True, blank=True)
    degree_type = models.CharField(max_length=100, choices=DEGREE_TYPE_CHOICES)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.degree_type} {self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Education: {self.degree_type} from {self.school_name}"  
     
class CertificationLicense(models.Model):
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    certification_file = models.FileField(upload_to='certificationsEducation/')
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.document_name} {self.education.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.document_name

class Experience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    company_phone = models.CharField(max_length=20)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="tell about your specific roles", max_length=500, null=True, blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.job_title} {self.user.username}"
            self.slug = unique_slug(value,type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Experience: {self.job_title} at {self.company_name}"

class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

class Position(models.Model):
    position = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='positions')
    skill_test_link = models.URLField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.position} {self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.position

class Skill(models.Model):
    skill = models.CharField(max_length=200)
    position = models.ManyToManyField(Position, related_name='skills')

    def __str__(self):
        return self.skill

class EmployeePreferences(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=2)
    salary_type = models.CharField(max_length=20, choices=SALARY_TYPES)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    can_relocation = models.CharField(max_length=10, choices=RELOCATION)
    years_of_experience = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desired_positions = models.ManyToManyField(Position, related_name='employee_preferences')
    skills = models.ManyToManyField(Skill)
    custom_positions = models.CharField(max_length=200, null=True, blank=True)
    custom_skills = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.job_type} {self.user.username}"
            self.slug = unique_slug(value, type(self))

        super().save(*args, **kwargs)  # Save the object
        
    def __str__(self):
        return f"{self.user.username}'s Preferences"

    def get_absolute_url(self):
        return reverse('employee:employee-preferences-detail', kwargs={'slug': self.slug})

    @property
    def positions_cache_key(self):
        return f"employee_positions_{self.category_id}"

    @property
    def skills_cache_key(self):
        return f"employee_skills_{self.desired_positions.values_list('id', flat=True)}"

    def get_positions(self):
        positions = cache.get(self.positions_cache_key)
        if not positions:
            positions = Position.objects.filter(category=self.category)
            cache.set(self.positions_cache_key, positions)
        return positions

    def get_skills(self):
        skills = cache.get(self.skills_cache_key)
        if not skills:
            skills = Skill.objects.filter(position__in=self.desired_positions.all())
            cache.set(self.skills_cache_key, skills)
        return skills


class SkillSetTestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    skill_test = models.CharField(max_length=200)
    states = models.CharField(max_length=20, choices=TEST_STATES, default="started")
    result = models.DecimalField(max_digits=5, decimal_places=2, default=00)
    conformation = models.CharField(max_length=200, default='Id12565874', null=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.user.username} {self.position}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Skill Set Test Result"

#Safety_Video_and_Test_completed
class Safety_Video_and_Test(models.Model):
    title = models.CharField(max_length=255 ,blank=True, null=True)
    image = models.ImageField(upload_to="Safety_Video_image/%Y/%m/%d" ,blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=500,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.title)
    
    #def get_absolute_url(self):
       # return reverse("employee:Safety_Video", kwargs={"pk": self.pk})
    
#VideoResume_completed
#class VideoResume(models.Model):
    #user, VideoResume, tell_about_you, tag, NumberViews, comments, slug, created, updated, 
    #pass

#Background_Check
#class Background_Check(models.Model):
    #user , uploadingW2 , uploadingW2, background_check_states,  slug, created, updated
    #pass