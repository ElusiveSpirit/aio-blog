from aiohttp.web_urldispatcher import View

from app.apps.auth.models import User
from app.utils.web_response import json_response


class UserView(View):

    async def get(self):
        user = [u async for u in User.connection.find()]
        return json_response({'users': user}, status=200)
