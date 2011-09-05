# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'CachedGeocode', fields ['lat']
        db.create_unique('geocodecache_cachedgeocode', ['lat'])

        # Adding unique constraint on 'CachedGeocode', fields ['lng']
        db.create_unique('geocodecache_cachedgeocode', ['lng'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'CachedGeocode', fields ['lng']
        db.delete_unique('geocodecache_cachedgeocode', ['lng'])

        # Removing unique constraint on 'CachedGeocode', fields ['lat']
        db.delete_unique('geocodecache_cachedgeocode', ['lat'])


    models = {
        'geocodecache.cachedgeocode': {
            'Meta': {'object_name': 'CachedGeocode'},
            'administrative_area': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'full_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'unique': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'unique': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geocodecache']
