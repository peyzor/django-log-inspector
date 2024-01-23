import io
import os
import zipfile
from itertools import islice

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView as _TemplateView

from . import settings
from .utils import get_log_entries, get_log_file_names

HTMX_STOP_POLLING = 286


class TemplateView(_TemplateView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(TemplateView, self).dispatch(*args, **kwargs)


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['custom_title'] = settings.LOG_INSPECTOR_FILE_LIST_TITLE
        context['custom_style_file'] = settings.LOG_INSPECTOR_FILE_LIST_STYLES
        return render(request, 'log_inspector/home.html', context=context)


class LogFileListView(TemplateView):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', '')

        log_filenames = get_log_file_names(settings.LOG_INSPECTOR_FILES_DIR)

        filenames = []
        for fn in log_filenames:
            if search and search.lower() not in fn:
                continue

            filenames.append(fn)

        context = {'filenames': filenames}
        return render(request, 'log_inspector/log_file_list.html', context=context)


class FileLogEntryListView(TemplateView):
    def get(self, request, filename, *args, **kwargs):
        if filename not in get_log_file_names(settings.LOG_INSPECTOR_FILES_DIR):
            raise Http404

        log_entries = get_log_entries(filename)

        max_lines = 1000
        paginator = Paginator(list(islice(log_entries, max_lines)), 20)

        page = request.GET.get('page', 1)

        try:
            log_entries = paginator.page(page)
        except PageNotAnInteger:
            log_entries = paginator.page(1)
        except EmptyPage:
            log_entries = paginator.page(paginator.num_pages)

        context = {'log_entries': log_entries, 'filename': filename}
        return render(request, 'log_inspector/file_log_entry_list.html', context)


class StartLiveView(TemplateView):
    def get(self, request, filename, *args, **kwargs):
        context = {'filename': filename}
        return render(request, 'log_inspector/start_live.html', context=context)


class StopLiveView(TemplateView):
    def get(self, request, filename, *args, **kwargs):
        context = {'filename': filename}
        return render(request, 'log_inspector/stop_live.html', context=context, status=HTMX_STOP_POLLING)


class DownloadLogFileView(TemplateView):
    def get(self, request, filename, *args, **kwargs):
        if filename not in get_log_file_names(settings.LOG_INSPECTOR_FILES_DIR):
            raise Http404

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.write(os.path.join(settings.LOG_INSPECTOR_FILES_DIR, filename))

        basename, _ = os.path.splitext(filename)
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{basename}.zip"'
        response.write(zip_buffer.getvalue())
        return response
