from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from uganda_common.utils import parse_telephone, parse_header_row, parse_name, parse_district, parse_village,\
    parse_birthdate, parse_gender, assign_backend
from xlrd import open_workbook
from rapidsms.models import Connection, Contact, Backend
from script.utils.handling import find_closest_match
from rapidsms.contrib.locations.models import Location
from bednets.spreadsheets_utils import XlsParser, is_empty, XlsParsingException
import re
from bednets import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
                Command to import HealthProviders by spreadsheet
                Expected to have headers --> ['telephone number', 'name','gender']
        """
        if len(args) < 1:
            print "Please specify file with reporters"
            return
        print handle_excel_file(open(args[0]))


def _clean_telephone_number(raw_number):
    raw_number = re.sub(" |-", "", raw_number)
    if raw_number[-2:] == '.0':
        raw_number = raw_number[:-2]
    if raw_number[:1] == '+':
        raw_number = raw_number[1:]
    return raw_number


def _parse_name(name):
    if is_empty(name):
        return "Anonymous User"
    return name.strip().title()


def _set_reporting_location(district, contact):
    if is_empty(district):
        contact.reporting_location = Location.tree.root_nodes()[0]
    contact.reporting_location = find_closest_match(district,
            Location.objects.filter(type__slug='district'))


def _get_unique_username(clean_name, suffix):
    name = clean_name + str(suffix) if suffix > 0 else clean_name
    try:
        User.objects.get(username=name)
        return _get_unique_username(clean_name, suffix+1)
    except User.DoesNotExist:
        return name


def _create_user_for_contact(values):
    user = User()
    name = values.get('name')
    if is_empty(name):
        user, created = User.objects.get_or_create(username='anonymous_user')
    else:
        name = name.strip()
        clean_name = name.replace(" ", "_").lower()
        unique_name = _get_unique_username(clean_name,0)
        user.username = unique_name
        user.first_name = name.title()
        user.email = 'mtrac@gmail.com'
        user.set_password('password')
    return user


def _assign_user_to_contact(contact, group, values):
    if contact.user is None:
        user = _create_user_for_contact(values)
        user.save()
    else:
        user = contact.user
    user.groups.add(group)
    user.save()
    contact.user = user
    contact.save()


def handle_excel_file(file):
    contacts = []
    invalid = []
    duplicates = []
    info = ''
    try:
        group = Group.objects.get(name=settings.BEDNETS_GROUP_NAME)
        parsed_values = XlsParser().parse(file.read())
        for values in parsed_values:
            raw_number = values.get('telephone number')
            if raw_number is None:
                invalid.append(values)
                continue
            raw_number = _clean_telephone_number(raw_number)
            if len(raw_number) < 9:
                invalid.append(raw_number)
                continue
            phone_number, backend = assign_backend(raw_number)
            if phone_number not in contacts and backend is not None:
                connection, created = Connection.objects.get_or_create(identity=phone_number, backend=backend)
                if not created and connection.contact is not None:
                    duplicates.append(phone_number)
                contact = connection.contact or Contact()
                contact.name = _parse_name(values.get('name'))
                _set_reporting_location(values.get('district'), contact)
                contact.save()
                contact.groups.add(group)
                _assign_user_to_contact(contact, group, values)
                connection.contact = contact
                connection.save()
                contacts.append(phone_number)
            elif backend is None:
                invalid.append(phone_number)
    except XlsParsingException:
        return "Invalid file"
    if len(contacts) > 0:
        info = 'Contacts with numbers... '\
               + ' ,'.join(contacts)\
        + ' have been uploaded ! '

    if len(duplicates) > 0:
        info = info\
               + 'The following numbers already exist in the system and have been updated: '\
        + ' ,'.join(duplicates)
    if len(invalid) > 0:
        info = info\
               + 'The following numbers may be invalid and thus have not been added to the system: '\
        + ' ,'.join(invalid)
    return info