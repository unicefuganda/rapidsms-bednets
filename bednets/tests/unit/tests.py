import unittest
from mtrack_project.rapidsms_cvs.cvs.tests.util import fake_incoming
from django.core.exceptions import ValidationError

class SendBednetsXformTest(unittest.TestCase):
    def test_should_invalidate_incomplete_message_without_number_of_bednets(self):
        message = fake_incoming('send')

        self.assertTrue(message.response.__contains__("Number of bednets is required."))

    def test_should_invalidate_incomplete_message_without_source(self):
        message = fake_incoming('send.11')

        self.assertTrue(message.response.__contains__("Location from which you are sending the bednets is required."))

    def test_should_invalidate_incomplete_message_without_destination(self):
        message = fake_incoming('send.11.from')

        self.assertTrue(message.response.__contains__("Location to which you are sending bednets is required."))

    def test_should_return_successful_response_for_complete_message(self):
        message = fake_incoming('send.11.from.to')

        self.assertTrue(message.response.__contains__("Thank you for your report!"))


class RecvBednetsXformTest(unittest.TestCase):
    def test_should_invalidate_incomplete_message_without_number_of_bednets(self):
        message = fake_incoming('recv')

        self.assertTrue(message.response.__contains__("Number of bednets received is required."))

    def test_should_invalidate_incomplete_message_without_received_at_location(self):
        message = fake_incoming('recv.11')

        self.assertTrue(message.response.__contains__("Location where bednets were received is  required."))


    def test_should_return_successful_response_for_complete_message(self):
        message = fake_incoming('recv.11.from')

        self.assertTrue(message.response.__contains__("Thank you for your report!"))


class DistBednetsXformTest(unittest.TestCase):
    def test_should_invalidate_incomplete_message_without_number_of_bednets(self):
        message = fake_incoming('dist')

        self.assertTrue(message.response.__contains__("Number of bednets distributed is required."))

    def test_should_invalidate_incomplete_message_without_received_at_location(self):
        message = fake_incoming('dist.11')

        self.assertTrue(message.response.__contains__("Location where bednets were distributed is required."))

    def test_should_return_successful_response_for_complete_message(self):
        message = fake_incoming('dist.11.from')

        self.assertTrue(message.response.__contains__("Thank you for your report!"))
