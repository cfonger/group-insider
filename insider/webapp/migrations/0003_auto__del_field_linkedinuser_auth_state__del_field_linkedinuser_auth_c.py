# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'LinkedInUser.auth_state'
        db.delete_column(u'webapp_linkedinuser', 'auth_state')

        # Deleting field 'LinkedInUser.auth_code'
        db.delete_column(u'webapp_linkedinuser', 'auth_code')

        # Adding field 'LinkedInUser.access_token'
        db.add_column(u'webapp_linkedinuser', 'access_token',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'LinkedInUser.expires_in'
        db.add_column(u'webapp_linkedinuser', 'expires_in',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'LinkedInUser.auth_state'
        db.add_column(u'webapp_linkedinuser', 'auth_state',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'LinkedInUser.auth_code'
        db.add_column(u'webapp_linkedinuser', 'auth_code',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'LinkedInUser.access_token'
        db.delete_column(u'webapp_linkedinuser', 'access_token')

        # Deleting field 'LinkedInUser.expires_in'
        db.delete_column(u'webapp_linkedinuser', 'expires_in')


    models = {
        u'webapp.linkedinuser': {
            'Meta': {'object_name': 'LinkedInUser'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'connections_json': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expires_in': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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