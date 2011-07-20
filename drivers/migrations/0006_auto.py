# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing M2M table for field vehicle on 'Driver'
        db.delete_table('drivers_driver_vehicle')


    def backwards(self, orm):
        
        # Adding M2M table for field vehicle on 'Driver'
        db.create_table('drivers_driver_vehicle', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('driver', models.ForeignKey(orm['drivers.driver'], null=False)),
            ('vehicle', models.ForeignKey(orm['vehicles.vehicle'], null=False))
        ))
        db.create_unique('drivers_driver_vehicle', ['driver_id', 'vehicle_id'])


    models = {
        'drivers.driver': {
            'Meta': {'object_name': 'Driver'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identification': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'img/nophoto.jpg'", 'max_length': '100'}),
            'telephone1': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['drivers']
