from django.db import connection, transaction

def send_submission_handler(submission):
    sub_county = submission.eav_values.all()[1].value
    distribution_point = submission.eav_values.all()[2].value
    quantity_sent_to_dp = submission.eav_values.all()[0].value
    query_dist = "update bednets_bednetsreport set quantity_sent_to_dp=quantity_sent_to_dp+" + str(quantity_sent_to_dp) \
                 + "where distribution_point='" + distribution_point + "'"
    cursor_recv_dist = run_sql(query_dist)
    if cursor_recv_dist.rowcount > 0:
        return
    from rapidsms_bednets.bednets.models import BednetsReport
    BednetsReport.objects.create(sub_county=sub_county, distribution_point=distribution_point,quantity_sent_to_dp=quantity_sent_to_dp)

def received_submission_handler(submission):
    received_at = submission.eav_values.all()[1].value #sc or dp
    quantity_received = submission.eav_values.all()[0].value
    query_recv = "update bednets_bednetsreport set quantity_received_at_dp=quantity_received_at_dp+" + \
                 str(quantity_received) + " where distribution_point='" + received_at + "'"
    run_sql(query_recv)
    query_recv_dist = "update bednets_bednetsreport set in_stock = quantity_received_at_dp - quantity_distributed_at_dp where distribution_point='" \
                      + received_at + "'"
    cursor_recv_dist = run_sql(query_recv_dist)
    if cursor_recv_dist.rowcount > 0:
        return
    query_recv_sc = "update bednets_bednetsreport set quantity_at_subcounty=quantity_at_subcounty+" +\
                    str(quantity_received) + " where sub_county='" + received_at + "'"
    cursor_recv_sc = run_sql(query_recv_sc)
    if cursor_recv_sc.rowcount > 0:
        return
    from rapidsms_bednets.bednets.models import BednetsReport
    BednetsReport.objects.create(sub_county=received_at, quantity_at_subcounty=quantity_received)

def dist_submission_handler(submission):
    distributed_at = submission.eav_values.all()[1].value
    quantity_distributed = submission.eav_values.all()[0].value
    query_dist = "update bednets_bednetsreport set quantity_distributed_at_dp=quantity_distributed_at_dp+" + \
                 str(quantity_distributed)+ " where distribution_point='" + distributed_at + "'"
    run_sql(query_dist)
    query_recv_dist = "update bednets_bednetsreport set in_stock = quantity_received_at_dp - quantity_distributed_at_dp where distribution_point='"\
                      + distributed_at + "'"
    cursor = run_sql(query_recv_dist)
    if cursor.rowcount > 0:
        return
    from rapidsms_bednets.bednets.models import BednetsReport
    BednetsReport.objects.create(distribution_point=distributed_at, quantity_distributed_at_dp=quantity_distributed)


def run_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return cursor



