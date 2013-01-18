# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DumpReport'
        db.create_table('bednets_dumpreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.TextField')(null=True)),
            ('telephone', self.gf('django.db.models.fields.TextField')()),
            ('district', self.gf('django.db.models.fields.TextField')(null=True)),
            ('invalid_submission', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invalid_reporter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('number_of_bednets', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('at_location', self.gf('django.db.models.fields.TextField')()),
            ('from_location', self.gf('django.db.models.fields.TextField')(null=True)),
            ('submission_id', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ))
        db.send_create_signal('bednets', ['DumpReport'])


    def backwards(self, orm):
        # Deleting model 'DumpReport'
        db.delete_table('bednets_dumpreport')


    models = {
        'bednets.bednetsreport': {
            'Meta': {'object_name': 'BednetsReport'},
            'distribution_point': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_stock': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'quantity_at_subcounty': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'quantity_distributed_at_dp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'quantity_received_at_dp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'quantity_sent_to_dp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'sub_county': ('django.db.models.fields.TextField', [], {})
        },
        'bednets.dumpreport': {
            'Meta': {'object_name': 'DumpReport'},
            'at_location': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'district': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'from_location': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invalid_reporter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invalid_submission': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keyword': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'number_of_bednets': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'telephone': ('django.db.models.fields.TextField', [], {}),
            'submission_id': ('django.db.models.fields.IntegerField', [], {})
            }
    }

    complete_apps = ['bednets']