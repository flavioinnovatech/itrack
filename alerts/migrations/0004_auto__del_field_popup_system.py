# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Popup.system'
        db.delete_column('alerts_popup', 'system_id')


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Popup.system'
        raise RuntimeError("Cannot reverse this migration. 'Popup.system' and its values cannot be restored.")


    models = {
        'alerts.alert': {
            'Meta': {'object_name': 'Alert'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destinataries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'geofence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geofence.Geofence']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linear_limit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'receive_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receive_popup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receive_sms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.System']"}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.CustomFieldName']", 'null': 'True'}),
            'vehicle': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['vehicles.Vehicle']", 'symmetrical': 'False'})
        },
        'alerts.popup': {
            'Meta': {'object_name': 'Popup'},
            'alert': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alerts.Alert']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vehicles.Vehicle']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'equipments.customfield': {
            'Meta': {'object_name': 'CustomField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'system': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['system.System']", 'symmetrical': 'False'}),
            'table': ('django.db.models.fields.IntegerField', [], {}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'tag'", 'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'equipments.customfieldname': {
            'Meta': {'object_name': 'CustomFieldName'},
            'custom_field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.CustomField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.System']"})
        },
        'equipments.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'serial': ('django.db.models.fields.CharField', [], {'default': "'000017E8'", 'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'system': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['system.System']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.EquipmentType']"})
        },
        'equipments.equipmenttype': {
            'Meta': {'object_name': 'EquipmentType'},
            'custom_field': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['equipments.CustomField']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'default': "'Quanta'", 'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'geofence.geofence': {
            'Meta': {'object_name': 'Geofence'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.System']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'system.system': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'System', '_ormbases': ['sites.Site']},
            'administrator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'usuarios'", 'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.System']", 'null': 'True', 'blank': 'True'}),
            'site_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True', 'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'vehicles.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            'chassi': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.Equipment']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_alert_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'license_plate': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'system': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['system.System']", 'null': 'True', 'symmetrical': 'False'}),
            'threshold_time': ('django.db.models.fields.FloatField', [], {'default': '5'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['alerts']
