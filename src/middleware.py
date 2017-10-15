from functools import wraps

from aiohttp.hdrs import METH_ALL


__all__ = [
    'middleware_db',
    'crossdomain',
]

async def middleware_db(app, handler):
    @wraps(handler)
    async def middleware_handler(request):
        async with app['db'].acquire() as conn:
            print('connect aiopg %r', conn)
            request['conn'] = conn
            result = await handler(request)

        print('connect aiopg close!')
        return result

    return middleware_handler


def set_default_headers(headers):
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = (
        'Cache-control, '
        'Accept, '
        'X-auth-token, '
        'Content-type, '
        'WWW-Authenticate')
    headers['Access-Control-Allow-Methods'] = ','.join(METH_ALL)


async def crossdomain(app, handler):
    @wraps(handler)
    async def middleware_handler(request):
        response = await handler(request)
        set_default_headers(response.headers)
        return response

    return middleware_handler
