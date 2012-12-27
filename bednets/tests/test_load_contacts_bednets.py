import unittest
from bednets.management.commands.load_contacts_bednets import _clean_telephone_number, \
    _parse_name, _parse_gender, _set_village
from mock import Mock

class LoadContactsBednetsTests(unittest.TestCase):

    def test_should_clean_spaces_and_dash_from_raw_number(self):
        self.assertEqual('256793449433',_clean_telephone_number('256 793449433'))
        self.assertEqual('256793449433',_clean_telephone_number('256-793449433'))

    def test_should_clean_trailing_point_zero_from_raw_number(self):
        self.assertEqual('256793449433',_clean_telephone_number('256793449433.0'))

    def test_should_clean_leading_plus_from_raw_number(self):
        self.assertEqual('256793449433',_clean_telephone_number('+256793449433'))

    def test_should_return_anonymous_user_for_empty_name(self):
        self.assertEqual('Anonymous User',_parse_name(None))
        self.assertEqual('Anonymous User',_parse_name('   '))

    def test_should_titalize_name(self):
        self.assertEqual('Akshay Naval',_parse_name('akshay naval  '))

    def test_should_parse_gender(self):
        self.assertEqual('M',_parse_gender('male'))
        self.assertEqual('F',_parse_gender('female'))
        self.assertEqual(None,_parse_gender(None))
        self.assertEqual(None,_parse_gender(''))

    def test_should_not_set_village_on_contact_if_village_is_empty(self):
        contact = Mock()
        contact.village = 'not_set'
        _set_village('  ',contact)
        self.assertAlmostEqual('not_set', contact.village)