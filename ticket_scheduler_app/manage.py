#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from scheduler.lib.logger import log_msg
from ticket_scheduler import settings


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_scheduler.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv \
            and 'seed' not in sys.argv and 'collectstatic' not in sys.argv:
        log_msg(f'sys argv = {sys.argv}')
        settings.IS_RUNNING = True

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
