from django.shortcuts  import render_to_response
from time import strftime
import datetime
from mtrack_project.rapidsms_mtrack.mtrack.utils import write_xls
from mtrack_project.rapidsms_xforms_src.rapidsms_xforms.models import XForm
import xlwt
from django.http import HttpResponse

def generate_excel_response(data, headings):
    book = xlwt.Workbook(encoding="utf8")
    write_xls(sheet_name="Bednets Reports", headings=headings, data=data, book=book)
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    fname_prefix = datetime.date.today().strftime('%Y%m%d') + "-" + strftime('%H%M%S')
    response["Content-Disposition"] = 'attachment; filename=%s_bednet_report.xls' % fname_prefix
    book.save(response)
    return response


def generate_bednets_report(request):
    sent_xform = XForm.objects.get(keyword="send")
    received_xform = XForm.objects.get(keyword="recv")
    distributed_xform = XForm.objects.get(keyword="dist")

    data=[]

    for sent_submission in sent_xform.submissions.all():
        data_builder = []
        data_builder.append(sent_submission.values.all()[1].value)
        data_builder.append(sent_submission.values.all()[0].value)
        data_builder.append(sent_submission.values.all()[2].value)

        received_quantity = 0
        dist_quantity = 0
        for received_submission in received_xform.submissions.all():
            if received_submission.values.all()[1].value == sent_submission.values.all()[2].value:
                received_quantity += received_submission.values.all()[0].value

        for dist_submission in distributed_xform.submissions.all():
            if dist_submission.values.all()[1].value == sent_submission.values.all()[2].value:
                dist_quantity += dist_submission.values.all()[0].value

        data_builder.append(received_quantity)
        data_builder.append(dist_quantity)
        data_builder.append(received_quantity - dist_quantity)

        data.append(data_builder)

    data = filter(None,data)
    headings = ["Sub-County", "Quantity sent to Distribution Point", "Distribution Point", "Quantity Received at Distribution Point", "Quantity Distributed at Distribution Point" ,"In Stock at Distribution Point"]

    return generate_excel_response(data, headings)


