import importlib
import logging
import logging.config
import os

from aiohttp.web import Application

from app.plugins import http_session
from app.utils import LazySettings
from app.middlewares.db_handler import db_handler
from app.utils.db import connect_db

logger = logging.getLogger(__name__)


def create_app():
    """Fabric creating web app"""
    from app.utils import settings

    os.environ.setdefault('AIOHTTP_SETTINGS_MODULE', 'config.settings.dev')

    app = Application()
    initialize_config(app, settings)
    initialize_db(app)

    initialize_routes(app)
    initialize_plugins(app)
    initialize_middlewares(app)

    return app


def initialize_config(app: Application, settings: LazySettings) -> None:
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    app['config'] = settings


def initialize_db(app: Application) -> None:
    client, db = connect_db()

    app.client = client
    app.db = db

    app.on_cleanup.append(close_db)
    initialize_models(app)


async def close_db(app: Application) -> None:
    app.client.close()
    await app.shutdown()


def initialize_models(app: Application) -> None:
    settings = app['config']

    def init_models(app_name: str) -> None:
        module_name = __name__.split('.')[0] + '.apps.' + app_name
        logger.info(f'Import module {module_name}')
        importlib.import_module(module_name)

    for app_name in settings.INSTALLED_APPS:
        init_models(app_name)


def initialize_routes(app: Application) -> None:
    from config.routes import routes
    api_prefix = app['config'].API_PREFIX

    for route in routes:
        app.router.add_route(route[0], api_prefix + route[1], route[2], name=route[3])


def initialize_plugins(app: Application) -> None:
    http_session.init_plugin(app)


def initialize_middlewares(app: Application) -> None:
    app.middlewares.append(db_handler(app.db))
