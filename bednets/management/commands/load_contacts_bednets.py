from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from uganda_common.utils import parse_telephone, parse_header_row, parse_name, parse_district, parse_village,\
    parse_birthdate, parse_gender, assign_backend
from xlrd import open_workbook
from rapidsms.models import Connection, Contact, Backend
from script.utils.handling import find_closest_match
from rapidsms.contrib.locations.models import Location
from bednets.spreadsheets_utils import XlsParser, is_empty, XlsParsingException
import re

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) < 1:
            print "Please specify file with reporters"
            return
#        fields = ['telephone number', 'name', 'district',
#                  'county', 'village', 'age',
#                  'gender', 'language']
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


def _parse_gender(gender):
    if is_empty(gender):
        return None
    return gender.upper()[:1]


def _set_village(village, contact):
    if is_empty(village):
        return
    _village = find_closest_match(village, Location.objects)
    if _village:
        contact.village = _village
        contact.village_name = _village.name or None


def _set_reporting_location(district, contact):
    if is_empty(district):
        contact.reporting_location = Location.tree.root_nodes()[0]
    contact.reporting_location = find_closest_match(district,
            Location.objects.filter(type__slug='district'))


def handle_excel_file(file):
    contacts = []
    invalid = []
    duplicates = []
    info = ''
    try:
        group, created = Group.objects.get_or_create(name="bednets")
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
                if not created:
                    duplicates.append(phone_number)
                    continue
                contact = connection.contact or Contact()
                contact.name = _parse_name(values.get('name'))
                contact.gender = _parse_gender(values.get('gender'))
                _set_village(values.get('village'), contact)
                _set_reporting_location(values.get('district'), contact)
                contact.save()
                contact.groups.add(group)
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
               + 'The following numbers already exist in the system and thus have not been uploaded: '\
        + ' ,'.join(duplicates)
    if len(invalid) > 0:
        info = info\
               + 'The following numbers may be invalid and thus have not been added to the system: '\
        + ' ,'.join(invalid)
    return info