from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import View

from app.apps.auth.models import User


class UserView(View):
    async def get(self):
        user = [u async for u in User.connection.find()]
        print('user', user)
        return json_response({
            'users': user
        }, status=200)
