import os
import sys
from datetime import *
from pprint import pprint

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import resolve, reverse
from django.db.models import *
from django.utils import timezone

from oauth2_provider.models import Application
from geo_django_rf.restapi.models import *


User = get_user_model()

if os.path.exists('/.dockerenv'):
    # save a history file to the project root if inside docker
    import atexit
    import readline
    from pathlib import Path

    hist_file = '.pyhistory'

    @atexit.register
    def save_history(hist_file=hist_file):
        import readline
        readline.write_history_file(hist_file)

    # touch
    Path(hist_file).touch()
    readline.read_history_file(hist_file)
    del atexit, readline, save_history, hist_file
