# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Driver.vehicle'
        db.delete_column('drivers_driver', 'vehicle_id')


    def backwards(self, orm):
        
        # Adding field 'Driver.vehicle'
        db.add_column('drivers_driver', 'vehicle', self.gf('django.db.models.fields.related.ForeignKey')(default='CXP1337', to=orm['vehicles.Vehicle']), keep_default=False)


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
