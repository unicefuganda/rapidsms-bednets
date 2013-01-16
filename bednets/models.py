from rapidsms.models import Contact
from bednets.spreadsheets_utils import is_empty
from django.db import models,transaction
from django.dispatch import receiver
from rapidsms_xforms.models import xform_received
from rapidsms_bednets.bednets.xformsubmissionhandlers import received_submission_handler,send_submission_handler,dist_submission_handler

class ConnectionProfile(object):

    def __init__(self, user):
        self.user = user

    @classmethod
    def lookup_by_connection(cls, connection):
        contact = Contact.objects.filter(connection=connection)
        return None if is_empty(contact) else ConnectionProfile(contact[0].user)

class BednetsReport(models.Model):
    sub_county = models.TextField()
    quantity_at_subcounty = models.IntegerField(null = True,default=0)
    quantity_sent_to_dp = models.IntegerField(null=True,default=0)
    distribution_point = models.TextField()
    quantity_received_at_dp = models.IntegerField(null=True,default=0)
    quantity_distributed_at_dp = models.IntegerField(null=True,default=0)
    in_stock = models.IntegerField(null=True,default=0)



handler  = {'send' : send_submission_handler, 'recv' : received_submission_handler, 'dist' : dist_submission_handler}

@receiver(xform_received)
def handle_submission(sender, **kwargs):
    xform = kwargs['xform']
    if xform.keyword not in handler.keys():
        return
    submission = kwargs['submission']
    update_reports(xform,submission)

@transaction.commit_manually
def update_reports(xform,submission):
    if submission.has_errors:
        print "\n\n\nSubmission had ERRORS"
        return
    try:
        handler[xform.keyword](submission)
        transaction.commit()
    except Exception as e:
        print "Rolling back\n" + str(e)
        transaction.rollback()



