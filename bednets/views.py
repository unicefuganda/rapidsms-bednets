from mtrack_project.rapidsms_bednets.bednets.view_helpers import generate_excel_response,generate_multiple_excel_sheets_response, get_outer_join_sent_recv_dist,get_data_dump_for_bednets, get_consolidated_data
from mtrack_project.rapidsms_xforms_src.rapidsms_xforms.models import XForm


def generate_bednets_report(request):
    data = get_consolidated_data()
    headings = ["Sub-County","Quantity Received at Sub-County" ,"Quantity sent to Distribution Point", "Distribution Point", "Quantity Received at Distribution Point", "Quantity Distributed at Distribution Point" ,"Quantity Received at DP - Quantity Distributed at DP"]

    return generate_excel_response(data, headings)

def generate_dump_bednets_report(request):
    sent_xform = XForm.objects.get(keyword="send")
    received_xform = XForm.objects.get(keyword="recv")
    distributed_xform = XForm.objects.get(keyword="dist")
    
    sent_data,received_data,dist_data = get_data_dump_for_bednets(sent_xform,received_xform,distributed_xform)
    sent_headings = ["Name", "Telephone Number","District","Invalid Submission","Invalid Reporter","Number of BedNets Sent","From Location","To Location"]
    received_headings = ["Name", "Telephone Number","District","Invalid Submission","Invalid Reporter","Number of BedNets Sent","At Location"]

    return generate_multiple_excel_sheets_response(sent_data,received_data,dist_data,sent_headings,received_headings)
    

