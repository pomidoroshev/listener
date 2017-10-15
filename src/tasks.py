import json

from aiohttp import WSCloseCode
from aiopg.sa import create_engine

import settings


__all__ = [
    'connect_db',
    'close_db',
    'start_listen',
    'stop_listen',
    'start_websocket',
    'stop_websocket',
]

async def connect_db(app):
    app['db'] = await create_engine(
        **settings.DATABASE, echo=True, enable_hstore=False, loop=app.loop)


async def close_db(app):
    engine = app['db']
    engine.close()
    await engine.wait_closed()


async def listen(app):
    async with app['db'].acquire() as conn:
        async with conn.connection.cursor() as cur:
            try:
                await cur.execute('LISTEN watchers')
                while True:
                    msg = await conn.connection.notifies.get()
                    action, table, id_, *data = msg.payload.split(',')
                    print('$$$', action, table, id_, data)
                    for ws in app['websockets']:
                        ws.send_str(json.dumps({
                            'action': action,
                            'item': {
                                'id': id_,
                                'data': data[0] if data else '',
                            }
                        }))
                
            except BaseException as err:
                print(err)
                await cur.execute('UNLISTEN watchers')
                raise


async def start_listen(app):
    app['db_listener'] = app.loop.create_task(listen(app))


async def stop_listen(app):
    app['db_listener'].cancel()
    await app['db_listener']


async def start_websocket(app):
    app['websockets'] = set()


async def stop_websocket(app):
    for websocket in app['websockets']:
        await websocket.close(
            code=WSCloseCode.GOING_AWAY,
            message='Server shutdown',
        )
