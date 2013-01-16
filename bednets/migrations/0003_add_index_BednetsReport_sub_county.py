# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'BednetsReport', fields ['distribution_point']
        db.create_index('bednets_bednetsreport', ['distribution_point'])
        db.create_index('bednets_bednetsreport', ['sub_county'])


    def backwards(self, orm):
        # Removing index on 'BednetsReport', fields ['distribution_point']
        db.delete_index('bednets_bednetsreport', ['distribution_point'])
        db.delete_index('bednets_bednetsreport', ['sub_county'])


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