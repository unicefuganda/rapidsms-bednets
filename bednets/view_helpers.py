import datetime
import xlwt
from time import strftime
from mtrack_project.rapidsms_mtrack.mtrack.utils import write_xls
from django.http import HttpResponse

def generate_excel_response(data, headings):
    book = xlwt.Workbook(encoding="utf8")
    write_xls(sheet_name="BedNets Report", headings=headings, data=data, book=book)
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    fname_prefix = datetime.date.today().strftime('%Y%m%d') + "-" + strftime('%H%M%S')
    response["Content-Disposition"] = 'attachment; filename=%s_bednet_report.xls' % fname_prefix
    book.save(response)
    return response

def generate_multiple_excel_sheets_response(sent_data,received_data,dist_data,sent_headings,recv_headings):
    book = xlwt.Workbook(encoding="utf8")
    write_xls(sheet_name="Sent Report", headings=sent_headings, data=sent_data, book=book)
    write_xls(sheet_name="Received Report", headings=recv_headings, data=received_data, book=book)
    write_xls(sheet_name="Distributed Report", headings=recv_headings, data=dist_data, book=book)
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    fname_prefix = datetime.date.today().strftime('%Y%m%d') + "-" + strftime('%H%M%S')
    response["Content-Disposition"] = 'attachment; filename=%s_bednet_report.xls' % fname_prefix
    book.save(response)
    return response

def get_outer_join_sent_recv_dist(distributed_xform, received_xform, sent_xform):
    data = []
    for sent_submission in sent_xform.submissions.all():
        if not sent_submission.has_errors:
            data_builder = []
            data_builder.append(sent_submission.values.all()[1].value)
            received_quantity = 0
            dist_quantity = 0
            received_at_subcounty = 0
            for received_submission in received_xform.submissions.all():
                if not received_submission.has_errors and received_submission.values.all()[1].value == sent_submission.values.all()[2].value:
                    received_quantity += received_submission.values.all()[0].value
                if not received_submission.has_errors and received_submission.values.all()[1].value == sent_submission.values.all()[1].value:
                    received_at_subcounty = received_submission.values.all()[0].value
            for dist_submission in distributed_xform.submissions.all():
                if not dist_submission.has_errors and dist_submission.values.all()[1].value == sent_submission.values.all()[2].value:
                    dist_quantity += dist_submission.values.all()[0].value

            data_builder.append(received_at_subcounty)
            data_builder.append(sent_submission.values.all()[0].value)
            data_builder.append(sent_submission.values.all()[2].value)

            data_builder.append(received_quantity)
            data_builder.append(dist_quantity)
            data_builder.append(received_quantity - dist_quantity)

            data.append(data_builder)

    for received_submission in received_xform.submissions.all():
        if not received_submission.has_errors:
            has_corresponding_sent = False
            for sent_submission in sent_xform.submissions.all():
                if received_submission.values.all()[1] == sent_submission.values.all()[1]:
                    has_corresponding_sent = True
                    break
            if not has_corresponding_sent:
                data.append([received_submission.values.all()[1].value,received_submission.values.all()[0].value])

    data = filter(None, data)
    return data

def get_data_dump_for_bednets(sent_xform, received_xform, distributed_xform):
    sent_data = []
    received_data = []
    dist_data = []
    for submission in sent_xform.submissions.all():
        data_builder = []
        data_builder.append(submission.connection.contact.name if submission.connection.contact else "")
        data_builder.append(submission.connection.identity)
        data_builder.append(submission.connection.contact.reporting_location.name if submission.connection.contact else "")
        data_builder.append(submission.has_errors)
        data_builder.append(submission.values.all()[0].value)
        data_builder.append(submission.values.all()[1].value if len(submission.values.all())>=2 else "")
        data_builder.append(submission.values.all()[2].value if len(submission.values.all())>=3 else "")
        sent_data.append(data_builder)
    for submission in received_xform.submissions.all():
        data_builder = []
        data_builder.append(submission.connection.contact.name if submission.connection.contact else "")
        data_builder.append(submission.connection.identity)
        data_builder.append(submission.connection.contact.reporting_location.name if submission.connection.contact else "")
        data_builder.append(submission.has_errors)
        data_builder.append(submission.values.all()[0].value)
        data_builder.append(submission.values.all()[1].value if len(submission.values.all())>=2 else "")
        received_data.append(data_builder)
    for submission in distributed_xform.submissions.all():
        data_builder = []
        data_builder.append(submission.connection.contact.name if submission.connection.contact else "")
        data_builder.append(submission.connection.identity)
        data_builder.append(submission.connection.contact.reporting_location.name if submission.connection.contact else "")
        data_builder.append(submission.has_errors)
        print submission.values.all()
        data_builder.append(submission.values.all()[0].value)
        data_builder.append(submission.values.all()[1].value if len(submission.values.all())>=2 else "")
        dist_data.append(data_builder)
    return sent_data,received_data,dist_data