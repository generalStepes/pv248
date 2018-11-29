from aiohttp import web
import sys

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get('/{name}', handle),
                web.post('/{name}', handle)])

web.run_app(app, port = sys.argv[1])
