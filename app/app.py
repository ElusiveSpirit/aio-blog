import logging
import logging.config

import motor.motor_asyncio
from aiohttp.web import Application

from app.plugins import http_session
from config.routes import routes
from app.middlewares.db_handler import db_handler
from config.settings import Settings


def create_app():
    """Fabric creating web app"""
    app = Application()
    initialize_config(app)
    initialize_db(app)

    initialize_routes(app)
    initialize_plugins(app)
    initialize_middlewares(app)

    return app


def initialize_config(app: Application) -> None:
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

    app['config'] = Settings()


def initialize_db(app: Application) -> None:
    config = app['config']

    app.client = motor.motor_asyncio.AsyncIOMotorClient(config.DATABASE_URL)
    app.db = app.client[config.DATABASE_NAME]

    app.on_cleanup.append(close_db)


async def close_db(app: Application) -> None:
    app.client.close()
    await app.shutdown()


def initialize_routes(app: Application) -> None:
    api_prefix = app['config'].API_PREFIX

    for route in routes:
        app.router.add_route(route[0], api_prefix + route[1], route[2], name=route[3])


def initialize_plugins(app: Application) -> None:
    http_session.init_plugin(app)


def initialize_middlewares(app: Application) -> None:
    app.middlewares.append(db_handler(app.db))
