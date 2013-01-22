import datetime
import xlwt
from time import strftime
from mtrack.utils import write_xls
from django.http import HttpResponse
from django.db import connection

def generate_excel_response(data, headings):
    book = xlwt.Workbook(encoding="utf8")
    write_xls(sheet_name="BedNets Report", headings=headings, data=data, book=book,cell_red_if_value="")
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    fname_prefix = datetime.date.today().strftime('%Y%m%d') + "-" + strftime('%H%M%S')
    response["Content-Disposition"] = 'attachment; filename=%s_bednet_report.xls' % fname_prefix
    book.save(response)
    return response

def generate_multiple_excel_sheets_response(sent_data,received_data,dist_data,sent_headings,recv_headings):
    book = xlwt.Workbook(encoding="utf8")
    write_xls(sheet_name="Sent Report", headings=sent_headings, data=sent_data, book=book,cell_red_if_value=True)
    write_xls(sheet_name="Received Report", headings=recv_headings, data=received_data, book=book,cell_red_if_value=True)
    write_xls(sheet_name="Distributed Report", headings=recv_headings, data=dist_data, book=book,cell_red_if_value=True)
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    fname_prefix = datetime.date.today().strftime('%Y%m%d') + "-" + strftime('%H%M%S')
    response["Content-Disposition"] = 'attachment; filename=%s_bednet_report.xls' % fname_prefix
    book.save(response)
    return response

def replace_zero_with_empty_string(data):
    for index,value_list in enumerate(data):
        data_builder = []
        for key,item in enumerate(value_list):
            if key==0:
                data_builder.append(item)
            elif key==1 or key==6:
                data_builder.append(" " if item==0  else item)
            elif key==2 or key==3:
                data_builder.append("" if item==0  else item)
            elif key==4 :
                data_builder.append("" if item==0 or value_list[2]=="" else item)
            elif key==5 :
                data_builder.append("" if item==0 or value_list[2]=="" or value_list[4]=="" else item)

        has_recv_at_sc = True if value_list[1]>0 else False
        data_builder = [" " if data_index>1 and has_recv_at_sc and item=="" else item for data_index,item in enumerate(data_builder) ]

        data[index] = data_builder
    return data


def execute_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    data = filter(None, data)
    return data


def get_consolidated_data():
    data = execute_sql("select sub_county,quantity_at_subcounty,quantity_sent_to_dp,distribution_point,quantity_received_at_dp,quantity_distributed_at_dp,in_stock  from bednets_bednetsreport")
    data = replace_zero_with_empty_string(data)
    return data

def get_data_dump(keyword):
    return execute_sql("select name,telephone,district,invalid_submission,invalid_reporter,number_of_bednets,at_location,from_location  "
                       "from bednets_dumpreport where keyword='" + keyword + "'")

