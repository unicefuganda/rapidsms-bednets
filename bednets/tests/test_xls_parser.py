import os
from unittest import TestCase
import xlwt
from bednets.spreadsheets_utils import XlsParser

class TestXlsParser(TestCase):
    def _write_to_xls(self, data):
        self.file_name = "test.xls"
        wb = xlwt.Workbook()
        ws = wb.add_sheet('test')
        for row_number, row in enumerate(data.split('\n')):
            for col_number, val in enumerate(row.split(',')):
                ws.write(row_number, col_number, val)
        wb.save(self.file_name)

    def setUp(self):
        data = """
                                                                 TELEPHONE_NUMBER,NAME,SEX,LOCATION,AGE

                                                                 7798987102,Akshay,male,kampala,24
                                                                 7798987103,Argha,male,kampala,22

                                                                 7798987105,Naval,male,kampala,23
                                                                 7798987106,Chris,male,kampala,25
                                                                 7798987107,Bharti,female,kampala,22

                                 """
        self._write_to_xls(data)
        self.parser = XlsParser()

    def test_should_parse_xls_contents(self):
        with open(self.file_name) as input_file:
            parsed_values = self.parser.parse(input_file.read())
            self.assertEqual(5, len(parsed_values))
            self.assertEqual({u"telephone_number": u'7798987102', u'name': u'Akshay',
                              u'sex': u'male', u'location': u'kampala', u'age': u'24'},
                parsed_values[0])

    def test_should_raise_exception_for_invalid_format(self):
        data = """




                                 """
        self._write_to_xls(data)
        with open(self.file_name) as input_file:
            with self.assertRaises(Exception):
                self.parser.parse(input_file.read())

    def test_should_parse_xls_contents_with_extra_field_values(self):
        data = """
                                                                 TELEPHONE_NUMBER,NAME,SEX,LOCATION,AGE

                                                                 7798987102,Akshay,male,kampala,24, extra field
                                                                 7798987103,Argha,male,kampala,22

                                                                 7798987105,Naval,male,kampala,23, extra field1
                                                                 7798987106,Chris,male,kampala,25
                                                                 7798987107,Bharti,female,kampala,22
        """
        self._write_to_xls(data)
        with open(self.file_name) as input_file:
            parsed_values = self.parser.parse(input_file.read())
            self.assertEqual(5, len(parsed_values))
            self.assertEqual({u"telephone_number": u'7798987102', u'name': u'Akshay',
                              u'sex': u'male', u'location': u'kampala', u'age': u'24'},
                parsed_values[0])

    def test_should_parse_xls_contents_less_field_values_than_header(self):
        data = """
                                                                 TELEPHONE_NUMBER,NAME,SEX,LOCATION,AGE

                                                                 7798987102,Akshay,male,kampala,24, extra field
                                                                 7798987103,Argha,,kampala,22

                                                                 7798987105,Naval,male,kampala,23, extra field1
                                                                 7798987106,Chris,male,kampala,25
                                                                 7798987107,Bharti,female,kampala,22
        """
        self._write_to_xls(data)
        with open(self.file_name) as input_file:
            parsed_values = self.parser.parse(input_file.read())
            self.assertEqual(5, len(parsed_values))
            self.assertEqual({u"telephone_number": u'7798987103', u'name': u'Argha',
                              u'sex': u'', u'location': u'kampala', u'age': u'22'},
                parsed_values[1])


    def tearDown(self):
        os.remove(self.file_name)
        pass

