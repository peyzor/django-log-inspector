import os
import re
from fnmatch import fnmatch
from os.path import isfile

from . import settings


def reverse_readlines(file, buf_size=8192, exclude=None):
    patterns = settings.LOG_INSPECTOR_PATTERNS

    segment = None
    offset = 0
    file.seek(0, os.SEEK_END)
    file_size = remaining_size = file.tell()

    while remaining_size > 0:
        offset = min(file_size, offset + buf_size)
        file.seek(file_size - offset)

        buffer = file.read(min(remaining_size, buf_size))

        # remove the file's last "\n" if it exists, only for the first buffer
        if remaining_size == file_size and buffer[-1] == '\n':
            buffer = buffer[:-1]

        remaining_size -= buf_size
        lines = buffer.split('\n')

        # append last chunk's segment to this chunk's last line
        if segment is not None:
            lines[-1] += segment

        segment = lines[0]
        lines = lines[1:]

        log = []
        for line in reversed(lines):
            log.append(line)

            if any([line.startswith(p) for p in patterns]):
                log_text = '\n'.join(log[::-1])

                if exclude and re.search(exclude, log_text):
                    continue

                yield log_text
                log.clear()

    if segment is not None:
        yield segment


def get_log_entries(filename):
    file_log = os.path.join(settings.LOG_INSPECTOR_FILES_DIR, filename)
    with open(file_log, encoding='utf8', errors='ignore') as file:
        yield from reverse_readlines(file, exclude=settings.LOG_INSPECTOR_EXCLUDE_TEXT_PATTERN)


def get_log_file_names(directory, search=''):
    filenames = []
    matched_file_names = []
    search_pattern = re.compile(search, re.IGNORECASE)

    with os.scandir(directory) as entries:
        for entry in entries:
            matched = fnmatch(entry.name, settings.LOG_INSPECTOR_FILES_PATTERN)
            specified = entry.name in settings.LOG_INSPECTOR_FILES

            if isfile(entry) and (matched or specified):
                filenames.append(entry.name)

    for fn in filenames:
        if search and not search_pattern.search(fn):
            continue

        matched_file_names.append(fn)

    return matched_file_names


def filter_log_entries(log_entries, search=''):
    for entry in log_entries:
        if not entry:
            continue

        search_pattern = re.compile(search, re.IGNORECASE)

        if search and not search_pattern.search(entry):
            continue

        yield entry


def is_valid_filename(filename):
    if filename not in get_log_file_names(settings.LOG_INSPECTOR_FILES_DIR):
        return False

    return True
