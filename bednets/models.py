from rapidsms.models import Contact
from bednets.spreadsheets_utils import is_empty
from django.contrib.auth.models import Group
from django.db import models,transaction
from django.dispatch import receiver
from rapidsms_xforms.models import xform_received
from bednets import settings
from bednets.xform_submission_handlers import received_submission_handler,send_submission_handler,dist_submission_handler

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
    submission_id = models.IntegerField()
    created = models.DateTimeField()


handler  = {'send' : send_submission_handler, 'recv' : received_submission_handler, 'dist' : dist_submission_handler}

@receiver(xform_received,dispatch_uid="uniqueId")
def handle_submission(sender, **kwargs):
    xform = kwargs['xform']
    if xform.keyword not in handler.keys():
        return
    submission = kwargs['submission']
    duplicate_bednets = update_dump_reports(xform,submission)
    update_reports(xform,submission, duplicate_bednets)

@transaction.commit_manually
def update_reports(xform,submission, duplicate_bednets):
    if submission.has_errors:
        return
    try:
        print duplicate_bednets
        handler[xform.keyword](submission, duplicate_bednets)
        transaction.commit()
    except Exception as e:
        print "Rolling back\n" + str(e)
        transaction.rollback()


def invalidate_submissions_if_duplicate(keyword, submission, at_location, from_location, telephone):
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    yesterday = datetime.now() - relativedelta(days=1)
    duplicates = DumpReport.objects.filter(keyword=keyword, telephone=telephone,
        at_location=at_location,from_location=from_location, created__gte = yesterday,
        invalid_submission = False)
    if len(duplicates) == 1:
        from rapidsms_xforms.models import XFormSubmission
        dump_report = duplicates[0]
        dump_report.invalid_submission = True
        dump_report.save()
        XFormSubmission.objects.filter(id=dump_report.submission_id).update(has_errors = True)
        return dump_report.number_of_bednets
    return 0


@transaction.commit_manually
def update_dump_reports(xform,submission):
    duplicate_bednets = 0
    try:
        keyword = xform.keyword
        contact = submission.connection.contact
        name = contact.name if contact else ""
        telephone = submission.connection.identity
        district = contact.reporting_location.name if contact and contact.reporting_location else ""
        invalid_submission = submission.has_errors
        invalid_reporter = contact_exists_and_belongs_to_group(contact,settings.BEDNETS_GROUP_NAME)
        eav_values = submission.eav_values.all()
        number_of_bednets = eav_values[0].value
        at_location = eav_values[1].value if keyword=="recv" or keyword=="dist" else eav_values[2].value
        from_location = eav_values[1].value if keyword=="send" else ""
        duplicate_bednets = invalidate_submissions_if_duplicate(keyword, submission,
            at_location, from_location, telephone)
        DumpReport.objects.create(keyword=keyword,name=name,telephone=telephone,
            district=district,invalid_submission=invalid_submission,
            invalid_reporter=invalid_reporter,number_of_bednets=number_of_bednets,
            at_location=at_location,from_location=from_location, submission_id = submission.id,
            created = submission.created)

        transaction.commit()
    except Exception as e:
        transaction.rollback()
        print str(e)
    return duplicate_bednets

def contact_exists_and_belongs_to_group(contact,group_name):
    if not contact:
        return True
    group = Group.objects.get(name=group_name)
    return not (group in contact.groups.all())
