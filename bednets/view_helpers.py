import datetime
import xlwt
from time import strftime
from mtrack_project.rapidsms_mtrack.mtrack.utils import write_xls
from django.http import HttpResponse
from django.contrib.auth.models import Group

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
    write_xls(sheet_name="Sent Report", headings=sent_headings, data=sent_data, book=book,cell_red_if_value=False)
    write_xls(sheet_name="Received Report", headings=recv_headings, data=received_data, book=book,cell_red_if_value=False)
    write_xls(sheet_name="Distributed Report", headings=recv_headings, data=dist_data, book=book,cell_red_if_value=False)
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    fname_prefix = datetime.date.today().strftime('%Y%m%d') + "-" + strftime('%H%M%S')
    response["Content-Disposition"] = 'attachment; filename=%s_bednet_report.xls' % fname_prefix
    book.save(response)
    return response

def replace_zero_with_empty_string(data):
    for index,value_list in enumerate(data):
        data_builder = []
        has_recv_at_sc = True if value_list[1]>0 else False
        for key,item in enumerate(value_list):
            if key==1 or key==0:
                data_builder.append(" " if item==0 else item)
            elif key==2 or key==3:
                data_builder.append("" if item==0  else item)
            elif key==4 :
                data_builder.append("" if item==0 or value_list[2]=="" else item)
            elif key==5 :
                data_builder.append("" if item==0 or value_list[2]=="" or value_list[4]=="" else item)

        data_builder = [" " if data_index > 1 and has_recv_at_sc and item=="" else item for data_index,item in enumerate(data_builder) ]

        data[index] = data_builder
    return data


def contact_exists_and_belongs_to_group(submission,group_name):
    if not submission.connection.contact:
        return False
    group = Group.objects.get(name=group_name)
    return group in submission.connection.contact.groups.all()


def get_data_dump_for_bednets(sent_xform, received_xform, distributed_xform):
    sent_data = []
    received_data = []
    dist_data = []
    for submission in sent_xform.submissions.all():
        data_builder = []
        data_builder.append(submission.connection.contact.name if submission.connection.contact else "")
        data_builder.append(submission.connection.identity)
        data_builder.append(submission.connection.contact.reporting_location.name if submission.connection.contact and submission.connection.contact.reporting_location else "")
        data_builder.append(submission.has_errors)
        data_builder.append(contact_exists_and_belongs_to_group(submission,group_name="LLIN"))
        data_builder.append(submission.eav_values.all()[0].value)
        data_builder.append(submission.eav_values.all()[1].value if len(submission.eav_values.all())>=2 else "")
        data_builder.append(submission.eav_values.all()[2].value if len(submission.eav_values.all())>=3 else "")
        sent_data.append(data_builder)
    for submission in received_xform.submissions.all():
        data_builder = []
        data_builder.append(submission.connection.contact.name if submission.connection.contact else "")
        data_builder.append(submission.connection.identity)
        data_builder.append(submission.connection.contact.reporting_location.name if submission.connection.contact and submission.connection.contact.reporting_location else "")
        data_builder.append(submission.has_errors)
        data_builder.append(contact_exists_and_belongs_to_group(submission,"LLIN"))
        data_builder.append(submission.eav_values.all()[0].value)
        data_builder.append(submission.eav_values.all()[1].value if len(submission.eav_values.all())>=2 else "")
        received_data.append(data_builder)
    for submission in distributed_xform.submissions.all():
        data_builder = []
        data_builder.append(submission.connection.contact.name if submission.connection.contact else "")
        data_builder.append(submission.connection.identity)
        data_builder.append(submission.connection.contact.reporting_location.name if submission.connection.contact and submission.connection.contact.reporting_location else "")
        data_builder.append(submission.has_errors)
        data_builder.append(contact_exists_and_belongs_to_group(submission,"LLIN"))
        data_builder.append(submission.eav_values.all()[0].value)
        data_builder.append(submission.eav_values.all()[1].value if len(submission.eav_values.all())>=2 else "")
        dist_data.append(data_builder)
    return sent_data,received_data,dist_data

def get_consolidated_data():
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("select sub_county,quantity_at_subcounty,quantity_sent_to_dp,distribution_point,quantity_received_at_dp,quantity_distributed_at_dp,in_stock  from bednets_bednetsreport")
    data =  cursor.fetchall()
    data = filter(None, data)
    data = replace_zero_with_empty_string(data)
    return data

