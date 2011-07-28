# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CachedGeocode.state'
        db.add_column('geocodecache_cachedgeocode', 'state', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)

        # Changing field 'CachedGeocode.city'
        db.alter_column('geocodecache_cachedgeocode', 'city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CachedGeocode.administrative_area'
        db.alter_column('geocodecache_cachedgeocode', 'administrative_area', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CachedGeocode.country'
        db.alter_column('geocodecache_cachedgeocode', 'country', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CachedGeocode.number'
        db.alter_column('geocodecache_cachedgeocode', 'number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'CachedGeocode.full_address'
        db.alter_column('geocodecache_cachedgeocode', 'full_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'CachedGeocode.street'
        db.alter_column('geocodecache_cachedgeocode', 'street', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CachedGeocode.postal_code'
        db.alter_column('geocodecache_cachedgeocode', 'postal_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))


    def backwards(self, orm):
        
        # Deleting field 'CachedGeocode.state'
        db.delete_column('geocodecache_cachedgeocode', 'state')

        # User chose to not deal with backwards NULL issues for 'CachedGeocode.city'
        raise RuntimeError("Cannot reverse this migration. 'CachedGeocode.city' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CachedGeocode.administrative_area'
        raise RuntimeError("Cannot reverse this migration. 'CachedGeocode.administrative_area' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CachedGeocode.country'
        raise RuntimeError("Cannot reverse this migration. 'CachedGeocode.country' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CachedGeocode.number'
        raise RuntimeError("Cannot reverse this migration. 'CachedGeocode.number' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CachedGeocode.full_address'
        raise RuntimeError("Cannot reverse this migration. 'CachedGeocode.full_address' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CachedGeocode.street'
        raise RuntimeError("Cannot reverse this migration. 'CachedGeocode.street' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CachedGeocode.postal_code'
        raise RuntimeError("Cannot reverse this migration. 'CachedGeocode.postal_code' and its values cannot be restored.")


    models = {
        'geocodecache.cachedgeocode': {
            'Meta': {'object_name': 'CachedGeocode'},
            'administrative_area': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'full_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geocodecache']
