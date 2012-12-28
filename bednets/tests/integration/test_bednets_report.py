import unittest
from mtrack_project.rapidsms_bednets.bednets.views import get_outer_join_sent_recv_dist
from mtrack_project.rapidsms_cvs.cvs.tests.util import fake_incoming
from mtrack_project.rapidsms_xforms_src.rapidsms_xforms.models import XForm, XFormSubmission

class BednetsReportTest(unittest.TestCase):

    def test_should_map_outer_join_on_single_row_for_sent_recv_dist_xforms(self):
        fake_incoming('send.100.scw.dp1')
        fake_incoming('recv.100.dp1')
        fake_incoming('dist.50.dp1')
        fake_incoming('dist.30.dp1')

        sent_xform = XForm.objects.get(keyword="send")
        received_xform = XForm.objects.get(keyword="recv")
        distributed_xform = XForm.objects.get(keyword="dist")

        join_sent_recv_dist_data = get_outer_join_sent_recv_dist(sent_xform=sent_xform, received_xform=received_xform,
            distributed_xform=distributed_xform)
        expected_list = ["scw",100,"dp1",100,80,20]

        self.assertTrue(len(join_sent_recv_dist_data),1)
        self.assertEquals(join_sent_recv_dist_data[0],expected_list)


    def test_should_map_outer_join_on_multiple_rowa_for_sent_recv_dist_xforms(self):
        fake_incoming('send.100.scw.dp1')
        fake_incoming('recv.100.dp1')
        fake_incoming('dist.50.dp1')
        fake_incoming('dist.30.dp1')

        fake_incoming('send.200.scw.dp2')
        fake_incoming('recv.200.dp2')
        fake_incoming('dist.100.dp2')
        fake_incoming('dist.50.dp2')

        sent_xform = XForm.objects.get(keyword="send")
        received_xform = XForm.objects.get(keyword="recv")
        distributed_xform = XForm.objects.get(keyword="dist")

        join_sent_recv_dist_data = get_outer_join_sent_recv_dist(sent_xform=sent_xform, received_xform=received_xform,
            distributed_xform=distributed_xform)
        expected_list = [["scw", 100, "dp1", 100, 80, 20],["scw", 200, "dp2", 200, 150, 50]]

        self.assertTrue(len(join_sent_recv_dist_data), 2)
        self.assertEquals(join_sent_recv_dist_data, expected_list)

    def tearDown(self):
        XFormSubmission.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        XFormSubmission.objects.all().delete()

