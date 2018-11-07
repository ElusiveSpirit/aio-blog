from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import View


class IndexView(View):

    async def get(self):
        return json_response({}, status=200)
