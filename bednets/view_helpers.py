import datetime
import xlwt
from time import strftime
from mtrack_project.rapidsms_mtrack.mtrack.utils import write_xls
from django.http import HttpResponse

def generate_excel_response(data, headings):
    book = xlwt.Workbook(encoding="utf8")
    write_xls(sheet_name="Bednets Reports", headings=headings, data=data, book=book)
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
            data_builder.append(sent_submission.values.all()[0].value)
            data_builder.append(sent_submission.values.all()[2].value)

            received_quantity = 0
            dist_quantity = 0
            for received_submission in received_xform.submissions.all():
                if not received_submission.has_errors and received_submission.values.all()[1].value == sent_submission.values.all()[2].value:
                    received_quantity += received_submission.values.all()[0].value

            for dist_submission in distributed_xform.submissions.all():
                if not dist_submission.has_errors and dist_submission.values.all()[1].value == sent_submission.values.all()[2].value:
                    dist_quantity += dist_submission.values.all()[0].value

            data_builder.append(received_quantity)
            data_builder.append(dist_quantity)
            data_builder.append(received_quantity - dist_quantity)

            data.append(data_builder)
    data = filter(None, data)
    return data
