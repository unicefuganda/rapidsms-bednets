import unittest
from cvs.tests.util import fake_incoming
from bednets.models  import BednetsReport,DumpReport
from rapidsms_xforms_src.rapidsms_xforms.models import XForm
from django.contrib.auth.models import User, Group
from rapidsms.models import Contact, Connection, Backend
from bednets import settings
from rapidsms_xforms.models import XFormSubmission


class BednetsReportTest(unittest.TestCase):
    def setUp(self):
        self.connection = self.make_connections()

    def test_should_add_single_row_with_only_sc_entry_in_bednets_report_table(self):
        fake_incoming('recv.100.sc1', self.connection)

        row = BednetsReport.objects.filter(sub_county="sc1")

        self.assertEquals(len(row),1)
        self.assertEquals(row[0].sub_county,"sc1")
        self.assertEquals(row[0].quantity_at_subcounty,100)

    def test_should_add_single_row_in_dump_reports_table(self):
        fake_incoming('recv.100.foosc', self.connection)
        row = DumpReport.objects.filter(keyword="recv")

        self.assertEquals(len(row),1)
        self.assertEquals(row[0].at_location,"foosc")
        self.assertEquals(row[0].number_of_bednets,100)
        self.assertEquals(row[0].invalid_submission,False)
        self.assertEquals(row[0].invalid_reporter,False)

    def test_should_invalidate_submission_if_same_message_in_24_hours(self):
        submission1 = fake_incoming('recv.100.foosc', self.connection)
        row = DumpReport.objects.filter(keyword="recv")

        self.assertEquals(len(row),1)
        self.assertEquals(row[0].invalid_submission,False)

        submission2 = fake_incoming('recv.100.foosc', self.connection)
        row = DumpReport.objects.filter(keyword="recv")

        self.assertEquals(len(row),2)
        self.assertEquals(row[0].invalid_submission,True)
        self.assertEquals(row[0].submission_id,submission1.id)
        self.assertEquals(row[1].invalid_submission,False)
        self.assertEquals(row[1].submission_id,submission2.id)

    def test_should_change_bednets_report_if_duplicate_submission(self):
        fake_incoming('recv.600.foosc1', self.connection)
        fake_incoming('recv.600.foosc2', self.connection)
        fake_incoming('recv.400.foosc1', self.connection)
        row = BednetsReport.objects.filter(sub_county__in = ["foosc1","foosc2"])

        self.assertEquals(len(row),2)
        self.assertEquals(row[0].sub_county,"foosc2")
        self.assertEquals(row[0].quantity_at_subcounty,600)

        self.assertEquals(row[1].sub_county,"foosc1")
        self.assertEquals(row[1].quantity_at_subcounty,400)

    def test_should_make_proper_report_after_complete_flow(self):
        fake_incoming('recv.600.sc1', self.connection)
        fake_incoming('send.600.sc1.dp1', self.connection)
        fake_incoming('recv.600.dp1', self.connection)
        fake_incoming('dist.500.dp1', self.connection)

        row = BednetsReport.objects.all()

        self.assertEquals(len(row),2)
        self.assertEquals(row[0].sub_county,"sc1")
        self.assertEquals(row[0].quantity_at_subcounty,600)

        self.assertEquals(row[1].sub_county,"sc1")
        self.assertEquals(row[1].quantity_sent_to_dp,600)
        self.assertEquals(row[1].quantity_received_at_dp,600)
        self.assertEquals(row[1].quantity_distributed_at_dp,500)
        self.assertEquals(row[1].in_stock,100)
        self.assertEquals(row[1].distribution_point,"dp1")

        row = DumpReport.objects.all()

        self.assertEquals(len(row),4)
        self.assertFalse(row[0].invalid_submission)
        self.assertFalse(row[1].invalid_submission)
        self.assertFalse(row[2].invalid_submission)
        self.assertFalse(row[3].invalid_submission)

        fake_incoming('recv.400.dp1', self.connection)
        row = BednetsReport.objects.all()

        self.assertEquals(len(row),2)
        self.assertEquals(row[1].quantity_received_at_dp,400)
        self.assertEquals(row[1].in_stock,-100)


    def tearDown(self):
        DumpReport.objects.all().delete()
        BednetsReport.objects.all().delete()
        XFormSubmission.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        BednetsReport.objects.all().delete()
        DumpReport.objects.all().delete()
        XFormSubmission.objects.all().delete()

    def make_connections(self):
        group, created = Group.objects.get_or_create(name=settings.BEDNETS_GROUP_NAME)
        user, created = User.objects.get_or_create(username='fred', email='daphne@velma.com')
        user.set_password('secret')
        user.groups.add(group)
        user.save()
        contact, created = Contact.objects.get_or_create(name='shaggy', user=user)
        contact.groups.add(group)
        contact.save()
        backend, created = Backend.objects.get_or_create(name='scoobydoo')
        backend.save()
        connection1, created = Connection.objects.get_or_create(identity='0794339344', backend=backend)
        connection1.contact = contact
        connection1.save()
        return connection1
