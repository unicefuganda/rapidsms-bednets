from django.contrib.auth.decorators import login_required
from bednets.view_helpers import generate_excel_response,generate_multiple_excel_sheets_response,\
     get_data_dump, get_consolidated_data


@login_required
def generate_bednets_report(request):
    data = get_consolidated_data()
    headings = ["Sub-County","Quantity Received at Sub-County" ,"Quantity sent to Distribution Point", "Distribution Point", "Quantity Received at Distribution Point", "Quantity Distributed at Distribution Point" ,"Quantity Received at DP - Quantity Distributed at DP"]
    return generate_excel_response(data, headings)

@login_required
def generate_dump_bednets_report(request):
    sent_data = get_data_dump(keyword="send")
    received_data = get_data_dump(keyword="recv")
    dist_data = get_data_dump(keyword="dist")
    sent_headings = ["Name", "Telephone Number","District","Invalid Submission","Invalid Reporter","Number of BedNets Sent","From Location","To Location"]
    received_headings = ["Name", "Telephone Number","District","Invalid Submission","Invalid Reporter","Number of BedNets Sent","At Location"]

    return generate_multiple_excel_sheets_response(sent_data,received_data,dist_data,sent_headings,received_headings)
    

