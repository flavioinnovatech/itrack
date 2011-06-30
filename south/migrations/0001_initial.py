# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MigrationHistory'
        db.create_table('south_migrationhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('migration', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('applied', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal('south', ['MigrationHistory'])


    def backwards(self, orm):
        
        # Deleting model 'MigrationHistory'
        db.delete_table('south_migrationhistory')


    models = {
        'south.migrationhistory': {
            'Meta': {'object_name': 'MigrationHistory'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'applied': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'migration': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['south']
