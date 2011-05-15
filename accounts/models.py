from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    profile = models.ForeignKey(User,unique=True)
    telephone = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)

    def __unicode__(self):
      return self.user.username
      
    profile.default = 1
