# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BednetsReport'
        db.create_table('bednets_bednetsreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sub_county', self.gf('django.db.models.fields.TextField')()),
            ('quantity_at_subcounty', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('quantity_sent_to_dp', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('distribution_point', self.gf('django.db.models.fields.TextField')()),
            ('quantity_received_at_dp', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('quantity_distributed_at_dp', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('in_stock', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('bednets', ['BednetsReport'])


    def backwards(self, orm):
        # Deleting model 'BednetsReport'
        db.delete_table('bednets_bednetsreport')


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
        }
    }

    complete_apps = ['bednets']