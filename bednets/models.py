from rapidsms.models import Contact
from bednets.spreadsheets_utils import is_empty
from django.db import models
#from bednets.signals import *
from django.core.signals import request_finished
from django.dispatch import receiver
from rapidsms_xforms.models import xform_received
class ConnectionProfile(object):

    def __init__(self, user):
        self.user = user

    @classmethod
    def lookup_by_connection(cls, connection):
        contact = Contact.objects.filter(connection=connection)
        return None if is_empty(contact) else ConnectionProfile(contact[0].user)

class BednetsReport(models.Model):
    sub_county = models.TextField()
    distribution_point = models.TextField()
    quantity_at_subcounty = models.IntegerField(null = True,default=0)
    quantity_sent_to_dp = models.IntegerField(null=True,default=0)
    quantity_received_at_dp = models.IntegerField(null=True,default=0)
    quantity_distributed_at_dp = models.IntegerField(null=True,default=0)


bednets = ['send', 'recv', 'dist']
@receiver(xform_received)

def handle_submission(sender, **kwargs):
    xform = kwargs['xform']

    if xform.keyword not in bednets:
        return
    submission = kwargs['submission']
    update_reports(xform,submission)

def update_reports(xform,submission):
    if submission.has_errors:
        return
    if xform.keyword == "send":
        try:
            sub_county = submission.eav_values.all()[1].value
            distribution_point = submission.eav_values.all()[2].value
            quantity_sent_to_dp = submission.eav_values.all()[0].value
            existing_records = BednetsReport.objects.filter(sub_county=sub_county)
            for record in existing_records:
                if record.distribution_point == distribution_point:
                    record.quantity_sent_to_dp += quantity_sent_to_dp
                    record.save()
                    return
            BednetsReport.objects.create(sub_county=sub_county,distribution_point=distribution_point,quantity_sent_to_dp=quantity_sent_to_dp)
        except Exception as e:
            print str(e)
        return

    elif xform.keyword == "recv":
        try:
            received_at = submission.eav_values.all()[1].value #sc or dp
            quantity_received = submission.eav_values.all()[0].value

            #if it was received at a DP
            dp_exists = BednetsReport.objects.filter(distribution_point=received_at) #should only be 1 entry for each DP
            if len(dp_exists) == 1:
                dp_exists[0].quantity_received_at_dp += quantity_received
                dp_exists[0].save()
                return

            elif len(dp_exists) == 0:
                subcounty_exists = BednetsReport.objects.filter(sub_county=received_at)
                for subcounty in subcounty_exists:
                    if subcounty.distribution_point == '':
                        subcounty.quantity_at_subcounty += quantity_received
                        subcounty.save()
                        return

            BednetsReport.objects.create(sub_county=received_at,quantity_at_subcounty=quantity_received)

        except Exception as e:
            print str(e)
        return

    elif xform.keyword == "dist":
        try:
            distributed_at = submission.eav_values.all()[1].value
            quantity_distributed = submission.eav_values.all()[0].value

            dp_exists = BednetsReport.objects.filter(distribution_point=distributed_at) #should only be 1 entry for each DP
            if len(dp_exists) == 1:
                dp_exists[0].quantity_distributed_at_dp += quantity_distributed
                dp_exists[0].save()
                return

            elif len(dp_exists) == 0:
                BednetsReport.objects.create(distribution_point=distributed_at,quantity_distributed_at_dp=quantity_distributed)
                return

        except Exception as e:
            print str(e)
        return
