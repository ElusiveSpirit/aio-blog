#!/usr/bin/env python

import os
from functools import wraps

import click

from app.utils import settings


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
def runserver():
    pass


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
