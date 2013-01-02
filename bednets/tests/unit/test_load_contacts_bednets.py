import unittest
from django.contrib.auth.models import Group, User
from bednets.management.commands.load_contacts_bednets import _clean_telephone_number, \
    _parse_name, _parse_gender, _set_village, _create_user_for_contact
from mock import Mock, patch

class LoadContactsBednetsTests(unittest.TestCase):

    def setUp(self):
        self.user_patcher = patch('bednets.management.commands.load_contacts_bednets.User')
        self.user_mock = self.user_patcher.start()
        self.user_mock.DoesNotExist = User.DoesNotExist

        self.object_mock = Mock()
        existing_user = Mock(spec=User)

        def _side_effect(*args, **kwargs):
            if kwargs['username'] in ['test','test1']:
                return existing_user
            else:
                raise User.DoesNotExist

        self.object_mock.get.side_effect = _side_effect
        self.user_mock.objects = self.object_mock

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

    def test_should_create_a_user_with_username_and_group(self):
        values = dict(name='Unique User  ')
        user = _create_user_for_contact(values)
        self.assertEqual('unique_user', user.username)
        self.assertEqual('mtrac@gmail.com', user.email)
        self.assertEqual('Unique User', user.first_name)

    def test_should_handle_uniqueness_of_username_before_creating_user(self):
        values = dict(name='test')
        user = _create_user_for_contact(values)
        self.assertEqual('test2', user.username)

    def test_should_send_back_anonymous_user_if_no_name_specified(self):
        mock_user = Mock(spec=User)
        self.object_mock.get_or_create.return_value = mock_user, True
        self.assertEqual(mock_user, _create_user_for_contact(dict()))

    def tearDown(self):
        self.user_patcher.stop()
