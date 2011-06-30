# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Driver'
        db.create_table('drivers_driver', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('vehicle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vehicles.Vehicle'])),
            ('identification', self.gf('django.db.models.fields.IntegerField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telephone1', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('telephone2', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(default='img/nophoto.jpg', max_length=100)),
        ))
        db.send_create_signal('drivers', ['Driver'])


    def backwards(self, orm):
        
        # Deleting model 'Driver'
        db.delete_table('drivers_driver')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'drivers.driver': {
            'Meta': {'object_name': 'Driver'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identification': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'img/nophoto.jpg'", 'max_length': '100'}),
            'telephone1': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vehicles.Vehicle']"})
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

    complete_apps = ['drivers']
