"""AIO Initialize Context."""
from aiohttp import ClientSession, TCPConnector


def init_plugin(app):
    app.cleanup_ctx.append(http_session)


async def http_session(app):
    """initialize and cleanup after stop webapp."""
    app['session'] = ClientSession(connector=TCPConnector(verify_ssl=False))

    yield

    await app['session'].close()
