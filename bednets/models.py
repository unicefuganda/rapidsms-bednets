from rapidsms.models import Contact
from bednets.spreadsheets_utils import is_empty

class ConnectionProfile(object):

    def __init__(self, user):
        self.user = user

    @classmethod
    def lookup_by_connection(cls, connection):
        contact = Contact.objects.filter(connection=connection)
        return None if is_empty(contact) else ConnectionProfile(contact[0].user)