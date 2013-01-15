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
        data[index] = ["" if item==0 else item for item in value_list]
    return data

def get_outer_join_sent_recv_dist(distributed_xform, received_xform, sent_xform):
    data = []
    received_submissions = received_xform.submissions.all()
    distributed_submissions = distributed_xform.submissions.all()
    for sent_submission in sent_xform.submissions.all():
        if not sent_submission.has_errors:
            data_builder = []
            data_builder.append(sent_submission.eav_values.all()[1].value)
            received_quantity = 0
            dist_quantity = 0
            received_at_subcounty = 0
            for received_submission in received_submissions:
                if not received_submission.has_errors and received_submission.eav_values.all()[1].value == sent_submission.eav_values.all()[2].value:
                    received_quantity += received_submission.eav_values.all()[0].value
                if not received_submission.has_errors and received_submission.eav_values.all()[1].value == sent_submission.eav_values.all()[1].value:
                    received_at_subcounty = received_submission.eav_values.all()[0].value
            for dist_submission in distributed_submissions:
                if not dist_submission.has_errors and dist_submission.eav_values.all()[1].value == sent_submission.eav_values.all()[2].value:
                    dist_quantity += dist_submission.eav_values.all()[0].value

            data_builder.append(received_at_subcounty)
            data_builder.append(sent_submission.eav_values.all()[0].value)
            data_builder.append(sent_submission.eav_values.all()[2].value)

            data_builder.append(received_quantity)
            data_builder.append(dist_quantity)
            in_stock = received_quantity - dist_quantity

            data_builder.append(in_stock if in_stock!=0 else " ") #an empty string would mean the CELL is colored RED.Not what we want here.

            data.append(data_builder)

    for received_submission in received_submissions:
        if not received_submission.has_errors:
            has_corresponding_sent = False
            for sent_submission in sent_xform.submissions.all():
                if received_submission.eav_values.all()[1].value == sent_submission.eav_values.all()[2].value:
                    has_corresponding_sent = True
                    break
            if not has_corresponding_sent:
                data.append([received_submission.eav_values.all()[1].value,received_submission.eav_values.all()[0].value])

    data = filter(None, data)
    data = replace_zero_with_empty_string(data)
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

