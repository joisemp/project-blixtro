from django.db import models

# Create your models here.
class Organisation(models.Model):
    organisation_name = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)


