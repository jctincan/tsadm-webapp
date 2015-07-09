#!/usr/bin/env python3

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsadm.settings")
    os.environ.setdefault("TSADM_DEV", "true")
    os.environ.setdefault("TSADM_MODE", "dev")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
