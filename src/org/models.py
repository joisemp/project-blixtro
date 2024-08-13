from django.db import models


class Org(models.Model):
    org_name = models.CharField(max_length=255)
    org_full_name = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    address = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.org_name
    

class Department(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    head = models.OneToOneField('core.UserProfile', null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name    