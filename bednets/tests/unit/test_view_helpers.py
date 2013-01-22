import unittest
from bednets.view_helpers import replace_zero_with_empty_string

class BednetsReportTest(unittest.TestCase):

    def test_parsing_list_to_replace_recv_at_sc_and_instock_with_space_and_empty_string_for_all_other_zero_values(self):
        tuple = ("sc",0,0,"",0,0,0)
        expected_list = ["sc"," ","","","",""," "]

        parsed_list = replace_zero_with_empty_string([tuple])

        self.assertEquals(parsed_list,[expected_list])

    def test_parsing_list_to_replace_space_for_all_other_zero_values_where_recv_at_sc_exists(self):
        tuple = ("sc",100,0,"",0,0,0)
        expected_list = ["sc",100," "," "," "," "," "]

        parsed_list = replace_zero_with_empty_string([tuple])

        self.assertEquals(parsed_list,[expected_list])