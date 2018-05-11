#!/usr/bin/env python
import os
import subprocess
import sys
from subprocess import call

import django
from django.db import OperationalError

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PSCPACourseWork.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if 'do_test' in sys.argv:
        subprocess.call('python manage.py test > o.txt 2> s.txt', shell=True)
        if 'FAILED (failures=' in open('s.txt', 'r').read():
            print(open('s.txt', 'r').read())
            raise OperationalError()
        else:
            sys.exit(0)

    # if 'test' in sys.argv:
    #     try:
    #         execute_from_command_line(sys.argv)
    #     except OperationalError:
    #         pass
    # else:
    execute_from_command_line(sys.argv)
