from django.db import models

class Equipment(models.Model):
   name = models.CharField(max_length=200)
   #fields = models.ManyToManyField(CustomField)
   type = models.CharField(max_length=50)
   available = models.BooleanField()
   def __unicode__(self):
      return self.name

class CustomField(models.Model):
   name = models.CharField(max_length=200)
   type = models.CharField(max_length=50)
   available = models.BooleanField()
   table = models.IntegerField()
   def __unicode__(self):
      return self.name


class CustomFieldData(models.Model):
   customfield = models.ForeignKey(CustomField)
   name = models.CharField(max_length=200)
   value = models.BigIntegerField()
   type = models.CharField(max_length=50)
   def __unicode__(self):
      return self.name


   

