from aiohttp.web_response import json_response as aiohttp_json_response
from bson.json_util import dumps as bson_dumps


def json_response(dumps=bson_dumps, *args, **kwargs):
    return aiohttp_json_response(dumps=dumps, *args, **kwargs)
