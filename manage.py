#!/usr/bin/env python3
# $Id: manage.py 11966 2014-10-23 22:59:19Z jrms $

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsadm.settings")
    os.environ.setdefault("TSADM_DEV", "true")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
