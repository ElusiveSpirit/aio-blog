from aiohttp.web_response import json_response as aiohttp_json_response
from bson.json_util import dumps as bson_dumps


def json_response(*args, **kwargs):
    kwargs['dumps'] = kwargs.get('dumps', bson_dumps)
    return aiohttp_json_response(*args, **kwargs)
