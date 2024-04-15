import django

if django.VERSION >= (2, 0):
    from django.urls import re_path
else:
    from django.conf.urls import url as re_path

from .views import LogEntriesView, LogFilesView, HomeView, StartLiveView, DownloadLogFileView

app_name = "log_inspector"

urlpatterns = [
    re_path(r"^$", HomeView.as_view(), name='home'),
    re_path(r'^log-files/$', LogFilesView.as_view(), name='log_files'),
    re_path(r'^log-entries/(?P<filename>[\w\.-]+)/$', LogEntriesView.as_view(), name='log_entries'),
    re_path(r'^start-live/(?P<filename>[\w\.-]+)/$', StartLiveView.as_view(), name='start_live'),
    re_path(r'^download/(?P<filename>[\w\.-]+)/$', DownloadLogFileView.as_view(), name='download'),
]
