import unittest
from mtrack_project.rapidsms_cvs.cvs.tests.util import fake_incoming
from rapidsms_bednets.bednets.models  import BednetsReport,DumpReport,update_reports,update_dump_reports,handle_submission
from rapidsms_xforms_src.rapidsms_xforms.models import XForm

class BednetsReportTest(unittest.TestCase):

    def test_should_add_single_row_with_only_sc_entry_in_bednets_report_table(self):
        submission = fake_incoming('recv.100.sc1')
        submission.has_errors = False
        submission.save()

        xform = XForm.objects.get(keyword="recv")
        update_reports(xform,submission)

        row = BednetsReport.objects.filter(sub_county="sc1")

        self.assertEquals(len(row),1)
        self.assertEquals(row[0].sub_county,"sc1")
        self.assertEquals(row[0].quantity_at_subcounty,100)

    def test_should_add_single_row_in_dump_reports_table(self):
        submission = fake_incoming('recv.100.foosc')
        row = DumpReport.objects.filter(keyword="recv")

        self.assertEquals(len(row),1)
        self.assertEquals(row[0].at_location,"foosc")
        self.assertEquals(row[0].number_of_bednets,100)
        self.assertEquals(row[0].invalid_submission,True)
        self.assertEquals(row[0].invalid_reporter,True)

    def tearDown(self):
        DumpReport.objects.all().delete()
        BednetsReport.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        BednetsReport.objects.all().delete()
        DumpReport.objects.all().delete()

