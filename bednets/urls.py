from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from bednets.views import generate_bednets_report, generate_dump_bednets_report

urlpatterns = patterns('',
    url(r'^$',login_required(direct_to_template),{'template':'bednets/bednets.html'},name='bednets'),
    url(r'^report/$',generate_bednets_report ,name="bednets_excel_report"),
    url(r'^dump/$',generate_dump_bednets_report ,name="bednets_data_dump"),
)
