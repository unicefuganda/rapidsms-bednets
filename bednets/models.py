from rapidsms.models import Contact
from bednets.spreadsheets_utils import is_empty
from django.contrib.auth.models import Group
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

class DumpReport(models.Model):
    keyword = models.TextField()
    name = models.TextField(null=True)
    telephone = models.TextField()
    district = models.TextField(null=True)
    invalid_submission = models.BooleanField(default=False)
    invalid_reporter = models.BooleanField(default=False)
    number_of_bednets = models.IntegerField(default=0)
    at_location = models.TextField()
    from_location = models.TextField(null=True)



handler  = {'send' : send_submission_handler, 'recv' : received_submission_handler, 'dist' : dist_submission_handler}

@receiver(xform_received,dispatch_uid="uniqueId")
def handle_submission(sender, **kwargs):
    xform = kwargs['xform']
    if xform.keyword not in handler.keys():
        return
    submission = kwargs['submission']
    update_dump_reports(xform,submission)
    update_reports(xform,submission)

@transaction.commit_manually
def update_reports(xform,submission):
    if submission.has_errors:
        return
    try:
        handler[xform.keyword](submission)
        transaction.commit()
    except Exception as e:
        print "Rolling back\n" + str(e)
        transaction.rollback()

@transaction.commit_manually
def update_dump_reports(xform,submission):
    try:
        keyword = xform.keyword
        name = submission.connection.contact.name if submission.connection.contact else ""
        telephone = submission.connection.identity
        district = submission.connection.contact.reporting_location.name if submission.connection.contact and submission.connection.contact.reporting_location else ""
        invalid_submission = submission.has_errors
        invalid_reporter = contact_exists_and_belongs_to_group(submission,group_name="LLIN")
        number_of_bednets = submission.eav_values.all()[0].value
        at_location = submission.eav_values.all()[1].value if keyword=="recv" or keyword=="dist" else submission.eav_values.all()[2].value
        from_location = submission.eav_values.all()[1].value if keyword=="send" else ""
        DumpReport.objects.create(keyword=keyword,name=name,telephone=telephone,district=district,invalid_submission=invalid_submission,invalid_reporter=invalid_reporter,number_of_bednets=number_of_bednets,at_location=at_location,from_location=from_location)
        transaction.commit()
    except Exception as e:
        transaction.rollback()
        print str(e)

def contact_exists_and_belongs_to_group(submission,group_name):
    if not submission.connection.contact:
        return True
    group = Group.objects.get(name=group_name)
    return not (group in submission.connection.contact.groups.all())
