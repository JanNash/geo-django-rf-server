#!/usr/bin/env python3

import os
import sys


if __name__ == '__main__':

    DEFAULT_SETTINGS = 'geo_django_rf.settings'
    # DEFAULT_SETTINGS = (
    #     'geo_django_rf.settings.tests' if sys.argv[1:2] == ['test']
    #     else 'geo_django_rf.settings')

    if os.environ.get('DJANGO_SETTINGS_MODULE'
                      ) or os.path.isfile('/.dockerenv'):

        #
        # Vanilla Django startup
        #

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', DEFAULT_SETTINGS)
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

    else:

        #
        # Proxy manage.py calls to docker-compose
        #

        import subprocess

        EXPORT = []
        CONTAINER = 'web'
        HOST_PRERUN = None

        if sys.argv[:2][-1] == 'runserver':
            cmd = ['docker-compose', 'run', '--service-ports', CONTAINER,
                   'python'] + sys.argv + ['0.0.0.0:8000']
        elif sys.argv[:2][-1] == 'shell':
            cmd = ['docker-compose', 'run', '--rm',
                   '-e', 'PYTHONSTARTUP=.pythonrc.py',
                   CONTAINER, 'python'] + sys.argv
        else:
            cmd = ['docker-compose', 'run', '--rm', CONTAINER, 'python'] + sys.argv

        for env in EXPORT:
            env_val = os.environ.get(env)
            if env_val is not None:
                cmd.insert(2, '-e')
                cmd.insert(3, '{}={}'.format(env, env_val))

        def run_cmd():
            os.execvp(cmd[0], cmd)

        if HOST_PRERUN is not None:
            prerun_exit_code = subprocess.Popen(
                ['sh', '-c', HOST_PRERUN]).wait()
            if prerun_exit_code == 0:
                run_cmd()
            else:
                sys.exit(prerun_exit_code)
        else:
            run_cmd()
