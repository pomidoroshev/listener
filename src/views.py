import datetime
import json

import aiohttp
from aiohttp import web
from aiopg.sa.result import RowProxy

__all__ = [
    'index',
    'websocket',
]


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, RowProxy):
            return dict(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        return json.JSONEncoder.default(self, obj)


def dumps(data):
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder)


async def index(request):
    res = await request['conn'].execute('SELECT * FROM info')
    items = await res.fetchall()
    return web.json_response(items, dumps=dumps)


async def websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            print('###', msg.data)
            if msg.data == 'close':
                request.app['websockets'].discard(ws)
                await ws.close()

            elif msg.data.startswith('open'):
                request.app['websockets'].add(ws)

            else:
                await ws.send_str(msg.data + '/answer')

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception', ws.exception())
            request.app['websockets'].discard(ws)

    request.app['websockets'].discard(ws)
    print('Websocket closed')
    return ws
