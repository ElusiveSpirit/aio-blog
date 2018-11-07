from aiohttp.web_middlewares import middleware


def db_handler(db):
    @middleware
    async def func(request, handler):
        if request.path.startswith('/_debugtoolbar'):
            response = await handler(request)
            return response

        request.db = db
        response = await handler(request)
        return response
    return func
