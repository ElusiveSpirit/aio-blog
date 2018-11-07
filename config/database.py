import motor.motor_asyncio


def init_db(app):
    config = app['config']

    app.client = motor.motor_asyncio.AsyncIOMotorClient(config['DATABASE_URL'])
    app.db = app.client[config['DATABASE_NAME']]
