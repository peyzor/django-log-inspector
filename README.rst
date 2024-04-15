=================
Django Log Inspector
=================

Django Log Inspector allows you to read & download log files in the admin page

Quick start
-----------

1. Django Log Inspector is available directly from `PyPI`_:

::

    pip install django-log-inspector


2. Add ``"log_viewer"`` to your ``INSTALLED_APPS`` setting like this

::

    INSTALLED_APPS = [
        ...
        "log_inspector",
    ]


3. Include the log viewer URLconf in your project ``urls.py`` like this

::

    path('logs/', include('log_inspector.urls')),


4. In your ``settings.py`` file create the following value

::

    LOG_INSPECTOR_FILES = ['logfile1', 'logfile2', ...]
    LOG_INSPECTOR_FILES_PATTERN = '*.log*'
    LOG_INSPECTOR_FILES_DIR = 'logs/'
    LOG_INSPECTOR_PAGE_LENGTH = 25       # total log lines per-page
    LOG_INSPECTOR_MAX_READ_LINES = 1000  # total log lines will be read
    LOG_INSPECTOR_FILE_LIST_MAX_ITEMS_PER_PAGE = 25 # Max log files loaded in Datatable per page
    LOG_INSPECTOR_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']
    LOG_INSPECTOR_EXCLUDE_TEXT_PATTERN = None  # String regex expression to exclude the log from line

    # Optionally you can set the next variables in order to customize the admin:
    LOG_INSPECTOR_FILE_LIST_TITLE = "Custom title"
    LOG_INSPECTOR_FILE_LIST_STYLES = "/static/css/my-custom.css"

.. _`PyPI`: https://pypi.org/project/django-log-inspector/