# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    profile = models.ForeignKey(User,unique=True)
    telephone = models.CharField(max_length=20,verbose_name = "Telefone")
    cellphone = models.CharField(max_length=20,verbose_name = "Celular")
    address = models.CharField(max_length=200,verbose_name = "Endereço")
    city = models.CharField(max_length=50,verbose_name = "Cidade")

    def __unicode__(self):
      return self.profile.username
      
    profile.default = 1
