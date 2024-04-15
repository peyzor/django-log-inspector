# Django Log Inspector

## _Fast and Live view to your log files_

![version](https://img.shields.io/badge/version-0.0.4-blue.svg)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)
<a href="https://github.com/peyzor/django-log-inspector"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>

Django Log Inspector offers real-time monitoring and analysis of log files in Django projects.
It delivers a fast and live view of log data, eliminating manual page refreshing.
With an intuitive interface and live update functionality, it streamlines log file management for easier issue tracking
and troubleshooting in Django applications.

Django Log Inspector is available directly from <a href="https://pypi.org/project/django-log-inspector/">PyPI</a>:

## Installation

```
pip install django-log-inspector
```

Add in INSTALLED_APPS

```
installed_apps = [
    ...
    'log_inspector',
]
```

Include in the URLconf

```
path('logs/', include('log_inspector.urls')),
```


## Settings

```
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
```