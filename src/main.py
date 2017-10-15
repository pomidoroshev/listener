import asyncio

from aiohttp import web
import aiohttp_autoreload

from middleware import *
from tasks import *
from views import *
import settings


if settings.DEBUG:
    aiohttp_autoreload.start()


def create_app():
    loop = asyncio.get_event_loop()
    app = web.Application(
        debug=settings.DEBUG, middlewares=[middleware_db, crossdomain], loop=loop)

    app.on_startup.append(connect_db)
    app.on_cleanup.append(close_db)

    app.on_startup.append(start_websocket)
    app.on_shutdown.append(stop_websocket)

    app.on_startup.append(start_listen)
    app.on_shutdown.append(stop_listen)

    app.router.add_route('*', '/', index)
    app.router.add_route('GET', '/ws', websocket)

    return app


if __name__ == '__main__':
    web.run_app(create_app(), port=8000)
