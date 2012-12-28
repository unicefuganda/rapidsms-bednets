from django.conf.urls.defaults import *
from mtrack_project.rapidsms_bednets.bednets.views import generate_bednets_report

urlpatterns = patterns('',
    url(r'^report/$',generate_bednets_report ,name="bednets_excel_report"),
)
