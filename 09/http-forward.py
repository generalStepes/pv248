from aiohttp import web
import sys

async def handle(request):
    print(request)
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)
    if request.body_exists:
        print(await request.read())

app = web.Application()
app.add_routes([web.get('/', handle),
                web.post('/', handle),
                web.get('/{name}', handle)])

web.run_app(app, port=sys.argv[1])
