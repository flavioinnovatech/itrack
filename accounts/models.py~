# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    profile = models.ForeignKey(User,unique=True)
    telephone = models.CharField(max_length=20,verbose_name = "Telefone",null=True,blank=True)
    cellphone = models.CharField(max_length=20,verbose_name = "Celular")
    address = models.CharField(max_length=200,verbose_name = "Endereço",null=True,blank=True)
    city = models.CharField(max_length=50,verbose_name = "Cidade",null=True,blank=True)

    def __unicode__(self):
      return self.profile.username
      
    profile.default = 1
