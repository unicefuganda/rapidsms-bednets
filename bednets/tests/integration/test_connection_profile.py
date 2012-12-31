from unittest import TestCase
from django.contrib.auth.models import User
from rapidsms.models import Contact, Connection, Backend
from bednets.models import ConnectionProfile

class TestConnectionProfile(TestCase):
    def test_should_return_user_for_connection(self):
        user, created = User.objects.get_or_create(username='fred', email='daphne@velma.com')
        user.set_password('secret')
        user.save()

        contact, created = Contact.objects.get_or_create(name='shaggy', user=user)
        contact.save()

        backend, created = Backend.objects.get_or_create(name='scoobydoo')
        backend.save()

        connection1, created = Connection.objects.get_or_create(identity='0794339344', backend=backend)
        connection1.contact = contact
        connection1.save()

        self.assertEqual(user, ConnectionProfile.lookup_by_connection(connection1))

    def test_should_return_none_if_no_user_for_connection(self):
        self.assertIsNone(ConnectionProfile.lookup_by_connection(Connection()))

