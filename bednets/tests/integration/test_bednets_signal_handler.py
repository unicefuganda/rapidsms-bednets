import unittest
from mtrack_project.rapidsms_cvs.cvs.tests.util import fake_incoming
from mtrack_project.rapidsms_bednets.bednets.models  import BednetsReport,update_reports
from mtrack_project.rapidsms_xforms_src.rapidsms_xforms.models import XForm,xform_received
class BednetsReportTest(unittest.TestCase):

    def test_should_add_single_row_with_only_sc_entry(self):
        submission = fake_incoming('recv.100.sc1')
        submission.has_errors = False
        submission.save()

        xform_received.connect(update_reports)
        row = BednetsReport.objects.filter(sub_county="sc1")

        self.assertEquals(len(row),1)
        self.assertEquals(row[0].sub_county,"sc1")
        self.assertEquals(row[0].quantity_at_subcounty,100)

    @classmethod
    def tearDownClass(cls):
        BednetsReport.objects.all().delete()

