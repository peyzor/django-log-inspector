# Django Log Inspector

## _Fast and Live view to your log files_

![version](https://img.shields.io/badge/version-0.0.9-blue.svg)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)
<a href="https://github.com/peyzor/django-log-inspector"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>

Django Log Inspector offers real-time monitoring and analysis of log files in Django projects.
It delivers a fast and live-view of log data, eliminating manual page refreshing.
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
path('logs/', include('log_inspector.urls'))
```

## Settings

The directory of log files in your project

```
LOG_INSPECTOR_FILES_DIR = 'logs/'
```

A file is included if the pattern is matched, or it is specified

```
LOG_INSPECTOR_FILES = ['logfile1', 'logfile2', ...] # default: []
LOG_INSPECTOR_FILES_PATTERN = '*.log*'            
```

You must specify the patterns in which your log files start with

#### Note: Make sure you have a formatter specified for your logs in django settings

```
LOG_INSPECTOR_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']
```

How logs are displayed

```
LOG_INSPECTOR_PAGE_LENGTH = 25             # total logs per-page
LOG_INSPECTOR_MAX_READ_LINES = 1000        # total logs that are read
LOG_INSPECTOR_EXCLUDE_TEXT_PATTERN = None  # String regex expression to exclude the log
```

Optionally you can set the next variables in order to customize

```
LOG_INSPECTOR_FILE_LIST_TITLE = "Custom title"               # default: None
LOG_INSPECTOR_FILE_LIST_STYLES = "/static/css/my-custom.css" # default: None
```

## Login

Logs are only accessible to logged-in superusers.
If your login URL is different from Django's default, specify it in your settings.

```
LOGIN_URL = '/my-custom-admin/login/'
```

## Static Files

Deploy static files by running the command

```
python manage.py collectstatic
```

## Finally

Start the development server and visit

```
http://127.0.0.1:8000/logs/
```