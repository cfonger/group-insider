# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'LinkedInUser.access_token'
        db.alter_column(u'webapp_linkedinuser', 'access_token', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

    def backwards(self, orm):

        # Changing field 'LinkedInUser.access_token'
        db.alter_column(u'webapp_linkedinuser', 'access_token', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    models = {
        u'webapp.linkedinuser': {
            'Meta': {'object_name': 'LinkedInUser'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
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