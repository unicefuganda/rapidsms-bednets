from django.shortcuts  import render_to_response
from mtrack_project.rapidsms_bednets.bednets.view_helpers import generate_excel_response, get_outer_join_sent_recv_dist
from mtrack_project.rapidsms_xforms_src.rapidsms_xforms.models import XForm


def generate_bednets_report(request):
    sent_xform = XForm.objects.get(keyword="send")
    received_xform = XForm.objects.get(keyword="recv")
    distributed_xform = XForm.objects.get(keyword="dist")
    data = get_outer_join_sent_recv_dist(distributed_xform, received_xform, sent_xform)
    headings = ["Sub-County", "Quantity sent to Distribution Point", "Distribution Point", "Quantity Received at Distribution Point", "Quantity Distributed at Distribution Point" ,"In Stock at Distribution Point"]

    return generate_excel_response(data, headings)


