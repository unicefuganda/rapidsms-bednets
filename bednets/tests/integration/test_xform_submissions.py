import unittest
from mtrack_project.rapidsms_cvs.cvs.tests.util import fake_incoming
from mtrack_project.rapidsms_xforms_src.rapidsms_xforms.models import XFormSubmission

class SentBednetsXformTest(unittest.TestCase):

    def test_should_map_valid_values_to_xform_fields(self):
        message = fake_incoming('send.112.from.to')
        values = message.submission_values()
        submission = XFormSubmission.objects.get(xform=message.xform)

        self.assertEquals(3,len(values))
        self.assertEquals(112, values[0].value)
        self.assertEquals("from", values[1].value)
        self.assertEquals("to", values[2].value)
        self.assertEquals('send.112.from.to', submission.raw)

    @classmethod
    def tearDownClass(cls):
        XFormSubmission.objects.all().delete()


class ReceivedBednetsXformTest(unittest.TestCase):

    def test_should_map_valid_values_to_xform_fields(self):
        message = fake_incoming('recv.112.at')
        values = message.submission_values()
        submission = XFormSubmission.objects.get(xform=message.xform)


        self.assertEquals(2,len(values))
        self.assertEquals(112, values[0].value)
        self.assertEquals("at", values[1].value)
        self.assertEquals("recv.112.at",submission.raw)

    @classmethod
    def tearDownClass(cls):
        XFormSubmission.objects.all().delete()

class DistributedBednetsXformTest(unittest.TestCase):

    def test_should_map_valid_values_to_xform_fields(self):
        message = fake_incoming('dist.100.at')
        values = message.submission_values()
        submission = XFormSubmission.objects.get(xform=message.xform)

        self.assertEquals(2,len(values))
        self.assertEquals(100, values[0].value)
        self.assertEquals("at", values[1].value)
        self.assertEquals('dist.100.at',submission.raw)

    @classmethod
    def tearDownClass(cls):
        XFormSubmission.objects.all().delete()
