# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Command.idcmd'
        db.add_column('command_command', 'idcmd', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Command.idcmd'
        db.delete_column('command_command', 'idcmd')


    models = {
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
        'command.command': {
            'Meta': {'object_name': 'Command'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'ON'", 'max_length': '10'}),
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vehicles.Vehicle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idcmd': ('django.db.models.fields.IntegerField', [], {}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.System']"}),
            'time_executed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_received': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.CustomFieldName']", 'null': 'True'})
        },
        'command.cprsession': {
            'Meta': {'object_name': 'CPRSession'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'product_id': ('django.db.models.fields.IntegerField', [], {'default': '41'})
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
            'sessiontime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True', 'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'vehicles.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            'chassi': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.Equipment']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'erased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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

    complete_apps = ['command']
