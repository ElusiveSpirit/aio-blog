#!/usr/bin/env python

import os
import sys
from functools import wraps

import click
from aiohttp_debugtoolbar.panels import traceback
from aiohttp_devtools.cli import host_help, debugtoolbar_help, app_factory_help, port_help, aux_port_help, verbose_help
from aiohttp_devtools.exceptions import AiohttpDevException
from aiohttp_devtools.logs import setup_logging, main_logger
from aiohttp_devtools.runserver import runserver as _runserver, run_app, INFER_HOST

from app.utils import settings

_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=False)
_file_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=True)
_dir_may_exist = click.Path(dir_okay=True, file_okay=False, writable=True, resolve_path=True)


def setup():
    """
    Set up the application:
        - configure settings
        - connect db
    """
    from app.utils.db import connect_db

    # settings.configure()
    connect_db()


def setup_app_env(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        setup()
        return func(*args, **kwargs)
    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.argument('app-path', envvar='AIO_APP_PATH', type=_file_dir_existing, default='app')
@click.option('--host', default=INFER_HOST, help=host_help)
@click.option('--debug-toolbar/--no-debug-toolbar', envvar='AIO_DEBUG_TOOLBAR', default=None, help=debugtoolbar_help)
@click.option('--app-factory', 'app_factory_name', envvar='AIO_APP_FACTORY', help=app_factory_help)
@click.option('-p', '--port', 'main_port', envvar='AIO_PORT', type=click.INT, help=port_help)
@click.option('--aux-port', envvar='AIO_AUX_PORT', type=click.INT, help=aux_port_help)
@click.option('-v', '--verbose', is_flag=True, help=verbose_help)
def runserver(**config):
    """
    Run a development server for an aiohttp apps.
    Takes one argument "app-path" which should be a path to either a directory containing a recognized default file
    ("app.py" or "main.py") or to a specific file. Defaults to the environment variable "AIO_APP_PATH" or ".".
    The app path is run directly, see the "--app-factory" option for details on how an app is loaded from a python
    module.
    """
    active_config = {k: v for k, v in config.items() if v is not None}
    setup_logging(config['verbose'])
    try:
        run_app(*_runserver(**active_config))
    except AiohttpDevException as e:
        if config['verbose']:
            tb = click.style(traceback.format_exc().strip('\n'), fg='white', dim=True)
            main_logger.warning('AiohttpDevException traceback:\n%s', tb)
        main_logger.error('Error: %s', e)
        sys.exit(2)


@cli.command()
@click.option('--ipython', default=True)
@setup_app_env
def shell(ipython):
    def run_ipython():
        from IPython import start_ipython
        start_ipython(argv=[])

    def run_python():
        import code

        imported_objects = {
            'settings': settings
        }

        code.interact(local=imported_objects)

    if ipython is True or ipython == 'True':
        run_ipython()
    else:
        run_python()


if __name__ == '__main__':
    os.environ.setdefault('AIOHTTP_SETTINGS_MODULE', 'config.settings.dev')
    cli()
