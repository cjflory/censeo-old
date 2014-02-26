# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Meeting'
        db.create_table(u'censeo_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'censeo', ['Meeting'])

        # Adding M2M table for field voters on 'Meeting'
        m2m_table_name = db.shorten_name(u'censeo_meeting_voters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm[u'censeo.meeting'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meeting_id', 'user_id'])

        # Adding model 'Ticket'
        db.create_table(u'censeo_ticket', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tickets', to=orm['censeo.Meeting'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'censeo', ['Ticket'])

        # Adding model 'Vote'
        db.create_table(u'censeo_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_votes', to=orm['auth.User'])),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ticket_votes', to=orm['censeo.Ticket'])),
            ('story_point', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'censeo', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['user', 'ticket']
        db.create_unique(u'censeo_vote', ['user_id', 'ticket_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['user', 'ticket']
        db.delete_unique(u'censeo_vote', ['user_id', 'ticket_id'])

        # Deleting model 'Meeting'
        db.delete_table(u'censeo_meeting')

        # Removing M2M table for field voters on 'Meeting'
        db.delete_table(db.shorten_name(u'censeo_meeting_voters'))

        # Deleting model 'Ticket'
        db.delete_table(u'censeo_ticket')

        # Deleting model 'Vote'
        db.delete_table(u'censeo_vote')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'censeo.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'voters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'meetings_as_voter'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'censeo.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tickets'", 'to': u"orm['censeo.Meeting']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'censeo.vote': {
            'Meta': {'unique_together': "(('user', 'ticket'),)", 'object_name': 'Vote'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story_point': ('django.db.models.fields.FloatField', [], {}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ticket_votes'", 'to': u"orm['censeo.Ticket']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_votes'", 'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['censeo']