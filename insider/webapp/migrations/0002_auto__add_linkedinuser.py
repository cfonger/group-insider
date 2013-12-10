# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LinkedInUser'
        db.create_table(u'webapp_linkedinuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auth_code', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('auth_state', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('profile_json', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('connections_json', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'webapp', ['LinkedInUser'])


    def backwards(self, orm):
        # Deleting model 'LinkedInUser'
        db.delete_table(u'webapp_linkedinuser')


    models = {
        u'webapp.linkedinuser': {
            'Meta': {'object_name': 'LinkedInUser'},
            'auth_code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'auth_state': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'connections_json': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile_json': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'webapp.testmodel': {
            'Meta': {'object_name': 'TestModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'somefield': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['webapp']