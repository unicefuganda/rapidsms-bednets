import xlrd

def is_empty(arg):
    if arg is None:
        return True

    if isinstance(arg, basestring):
        arg = arg.strip()

    try:
        if not len(arg):
            return True
    except TypeError:
        # wasn't a sequence
        pass

    return False

class XlsParser(object):
    def parse(self, xls_contents):
        assert xls_contents is not None
        workbook = xlrd.open_workbook(file_contents=xls_contents)
        worksheet = workbook.sheets()[0]
        header_found = False
        header = None
        parsedData = []
        for row_num in range(worksheet.nrows):
            row = worksheet.row_values(row_num)

            if not header_found:
                header, header_found = self._is_header_row(row)
                continue
            if self._is_empty(row):
                continue

            row = self._clean(row)
            parsedData.append(dict(zip(header, row)))
        if not header_found:
            raise XlsParsingException()
        return parsedData

    def _remove_trailing_empty_header_field(self, field_header):
        for field in field_header[::-1]:
            if is_empty(field):
                field_header.pop()
            else:
                break

    def _is_header_row(self, row):
        if is_empty(row[0]):
            return None, False
        self._remove_trailing_empty_header_field(row)
        return [unicode(value).strip().lower() for value in row], True

    def _clean(self, row):
        return [unicode(value).strip() for value in row]

    def _is_empty(self, row):
        return len([value for value in row if not is_empty(value)]) == 0

class XlsParsingException(Exception):
    pass