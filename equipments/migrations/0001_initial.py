# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CustomField'
        db.create_table('equipments_customfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('table', self.gf('django.db.models.fields.IntegerField')()),
            ('tag', self.gf('django.db.models.fields.CharField')(default='tag', max_length=50)),
        ))
        db.send_create_signal('equipments', ['CustomField'])

        # Adding M2M table for field system on 'CustomField'
        db.create_table('equipments_customfield_system', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customfield', models.ForeignKey(orm['equipments.customfield'], null=False)),
            ('system', models.ForeignKey(orm['system.system'], null=False))
        ))
        db.create_unique('equipments_customfield_system', ['customfield_id', 'system_id'])

        # Adding model 'CustomFieldName'
        db.create_table('equipments_customfieldname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.System'])),
            ('custom_field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipments.CustomField'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('equipments', ['CustomFieldName'])

        # Adding model 'EquipmentType'
        db.create_table('equipments_equipmenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(default='Quanta', max_length=40)),
        ))
        db.send_create_signal('equipments', ['EquipmentType'])

        # Adding M2M table for field custom_field on 'EquipmentType'
        db.create_table('equipments_equipmenttype_custom_field', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipmenttype', models.ForeignKey(orm['equipments.equipmenttype'], null=False)),
            ('customfield', models.ForeignKey(orm['equipments.customfield'], null=False))
        ))
        db.create_unique('equipments_equipmenttype_custom_field', ['equipmenttype_id', 'customfield_id'])

        # Adding model 'AvailableFields'
        db.create_table('equipments_availablefields', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('equip_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipments.EquipmentType'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.System'])),
        ))
        db.send_create_signal('equipments', ['AvailableFields'])

        # Adding M2M table for field custom_fields on 'AvailableFields'
        db.create_table('equipments_availablefields_custom_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('availablefields', models.ForeignKey(orm['equipments.availablefields'], null=False)),
            ('customfield', models.ForeignKey(orm['equipments.customfield'], null=False))
        ))
        db.create_unique('equipments_availablefields_custom_fields', ['availablefields_id', 'customfield_id'])

        # Adding model 'Equipment'
        db.create_table('equipments_equipment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('serial', self.gf('django.db.models.fields.CharField')(default='000017E8', max_length=50, unique=True, null=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipments.EquipmentType'])),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('equipments', ['Equipment'])

        # Adding M2M table for field system on 'Equipment'
        db.create_table('equipments_equipment_system', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm['equipments.equipment'], null=False)),
            ('system', models.ForeignKey(orm['system.system'], null=False))
        ))
        db.create_unique('equipments_equipment_system', ['equipment_id', 'system_id'])

        # Adding model 'Tracking'
        db.create_table('equipments_tracking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('msgtype', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('equipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipments.Equipment'])),
            ('eventdate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('equipments', ['Tracking'])

        # Adding model 'TrackingData'
        db.create_table('equipments_trackingdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tracking', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipments.Tracking'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipments.CustomField'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('equipments', ['TrackingData'])

        # Adding model 'SystemPerms'
        db.create_table('equipments_systemperms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.System'], null=True)),
            ('google_map', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('google_geofence', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('maplink_map', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('multspectral_map', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('multspectral_geofence', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_sms', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('equipments', ['SystemPerms'])


    def backwards(self, orm):
        
        # Deleting model 'CustomField'
        db.delete_table('equipments_customfield')

        # Removing M2M table for field system on 'CustomField'
        db.delete_table('equipments_customfield_system')

        # Deleting model 'CustomFieldName'
        db.delete_table('equipments_customfieldname')

        # Deleting model 'EquipmentType'
        db.delete_table('equipments_equipmenttype')

        # Removing M2M table for field custom_field on 'EquipmentType'
        db.delete_table('equipments_equipmenttype_custom_field')

        # Deleting model 'AvailableFields'
        db.delete_table('equipments_availablefields')

        # Removing M2M table for field custom_fields on 'AvailableFields'
        db.delete_table('equipments_availablefields_custom_fields')

        # Deleting model 'Equipment'
        db.delete_table('equipments_equipment')

        # Removing M2M table for field system on 'Equipment'
        db.delete_table('equipments_equipment_system')

        # Deleting model 'Tracking'
        db.delete_table('equipments_tracking')

        # Deleting model 'TrackingData'
        db.delete_table('equipments_trackingdata')

        # Deleting model 'SystemPerms'
        db.delete_table('equipments_systemperms')


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
        'equipments.availablefields': {
            'Meta': {'object_name': 'AvailableFields'},
            'custom_fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['equipments.CustomField']", 'null': 'True', 'blank': 'True'}),
            'equip_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.EquipmentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.System']"})
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
        'equipments.systemperms': {
            'Meta': {'object_name': 'SystemPerms'},
            'can_sms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_geofence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_map': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maplink_map': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'multspectral_geofence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'multspectral_map': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.System']", 'null': 'True'})
        },
        'equipments.tracking': {
            'Meta': {'object_name': 'Tracking'},
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.Equipment']"}),
            'eventdate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msgtype': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'equipments.trackingdata': {
            'Meta': {'object_name': 'TrackingData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tracking': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.Tracking']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipments.CustomField']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        }
    }

    complete_apps = ['equipments']
