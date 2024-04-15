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
from .utils import get_log_entries, get_log_file_names, filter_log_entries, is_valid_filename

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


class LogFilesView(TemplateView):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', '')

        filenames = get_log_file_names(settings.LOG_INSPECTOR_FILES_DIR, search)
        filenames.sort()

        context = {'filenames': filenames}
        return render(request, 'log_inspector/log_files.html', context=context)


class LogEntriesView(TemplateView):
    def get(self, request, filename, *args, **kwargs):
        if not is_valid_filename(filename):
            raise Http404

        search = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        action = request.META.get('HTTP_X_ACTION')
        is_live_action = action == 'LIVE'

        log_entries = get_log_entries(filename)
        log_entries = filter_log_entries(log_entries, search)

        max_lines = settings.LOG_INSPECTOR_MAX_READ_LINES if not is_live_action else settings.LOG_INSPECTOR_PAGE_LENGTH
        paginator = Paginator(list(islice(log_entries, max_lines)), settings.LOG_INSPECTOR_PAGE_LENGTH)
        start_index = (int(page) - 1) * paginator.per_page

        try:
            log_entries = paginator.page(page)
        except PageNotAnInteger:
            log_entries = paginator.page(1)
        except EmptyPage:
            log_entries = paginator.page(paginator.num_pages)

        context = {'log_entries': log_entries, 'filename': filename, 'start_index': start_index}
        if is_live_action:
            return render(request, 'log_inspector/log_entries.html', context)

        return render(request, 'log_inspector/log_entries_table.html', context, status=HTMX_STOP_POLLING)


class StartLiveView(TemplateView):
    def get(self, request, filename, *args, **kwargs):
        context = {'filename': filename}
        return render(request, 'log_inspector/start_live.html', context=context)


class DownloadLogFileView(TemplateView):
    def get(self, request, filename, *args, **kwargs):
        if not is_valid_filename(filename):
            raise Http404

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.write(os.path.join(settings.LOG_INSPECTOR_FILES_DIR, filename))

        basename, _ = os.path.splitext(filename)
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{basename}.zip"'
        response.write(zip_buffer.getvalue())
        return response
