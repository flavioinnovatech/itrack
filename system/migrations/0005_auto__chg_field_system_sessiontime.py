# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'System.sessiontime'
        db.alter_column('system_system', 'sessiontime', self.gf('django.db.models.fields.IntegerField')())


    def backwards(self, orm):
        
        # Changing field 'System.sessiontime'
        db.alter_column('system_system', 'sessiontime', self.gf('django.db.models.fields.IntegerField')(null=True))


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
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'system.settings': {
            'Meta': {'object_name': 'Settings'},
            'color1': ('django.db.models.fields.CharField', [], {'default': "'#7a7a7a'", 'max_length': '50'}),
            'color2': ('django.db.models.fields.CharField', [], {'default': "'#ebebeb'", 'max_length': '50'}),
            'color_link': ('django.db.models.fields.CharField', [], {'default': "'#333333'", 'max_length': '50'}),
            'color_menu_font': ('django.db.models.fields.CharField', [], {'default': "'#e7e5e5'", 'max_length': '50'}),
            'color_menu_font_hover': ('django.db.models.fields.CharField', [], {'default': "'#444444'", 'max_length': '50'}),
            'color_site_background': ('django.db.models.fields.CharField', [], {'default': "'#e0e0e0'", 'max_length': '50'}),
            'color_site_font': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '50'}),
            'color_submenu_font': ('django.db.models.fields.CharField', [], {'default': "'#444444'", 'max_length': '50'}),
            'color_submenu_font_hover': ('django.db.models.fields.CharField', [], {'default': "'#e7e5e5'", 'max_length': '50'}),
            'color_submenu_gradient_final': ('django.db.models.fields.CharField', [], {'default': "'#cfcfcf'", 'max_length': '50'}),
            'color_submenu_gradient_inicial': ('django.db.models.fields.CharField', [], {'default': "'#ffffff'", 'max_length': '50'}),
            'color_submenu_hover': ('django.db.models.fields.CharField', [], {'default': "'#a0a0a0'", 'max_length': '50'}),
            'color_table_background': ('django.db.models.fields.CharField', [], {'default': "'#ffffff'", 'max_length': '50'}),
            'color_table_header': ('django.db.models.fields.CharField', [], {'default': "'#cccccc'", 'max_length': '50'}),
            'color_table_line_font_hover': ('django.db.models.fields.CharField', [], {'default': "'#212121'", 'max_length': '50'}),
            'color_table_line_hover': ('django.db.models.fields.CharField', [], {'default': "'#dadada'", 'max_length': '50'}),
            'css': ('django.db.models.fields.TextField', [], {'default': "'body {background-color:#E0E0E0}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "'img/logo.png'", 'max_length': '100'}),
            'map_google': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map_maplink': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map_multspectral': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['system.System']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'system.system': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'System', '_ormbases': ['sites.Site']},
            'administrator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'usuarios'", 'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.System']", 'null': 'True', 'blank': 'True'}),
            'sessiontime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True', 'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['system']
