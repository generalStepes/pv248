from aiohttp import web
import sys

routes = web.RouteTableDef()

sessionArr = []

class session:
  def __init__(self, id, playBoard, nextTurn, winner):
    self.id = id
    self.playBoard = playBoard
    self.nextTurn = nextTurn
    self.winner = winner

def isthereWinner(id, selectedSession, player):
    currentBoard = selectedSession.playBoard
    if currentBoard[0][0] == currentBoard[1][1] == currentBoard[2][2] == player or currentBoard[2][0] == currentBoard[1][1] == currentBoard[0][2] == player:
        sessionArr[id - 1].winner = player
    for x in range(0,3):
        if currentBoard[x][0] == currentBoard[x][1] == currentBoard[x][2] == player or currentBoard[0][x] == currentBoard[1][x] == currentBoard[2][x] == player:
            sessionArr[id - 1].winner = player
    if not any(0 in row for row in currentBoard):
        sessionArr[id - 1].winner = 0
    if sessionArr[id - 1].winner != -1: return True
    else: return False



def checkPlayer(selectedSession, id):
    if id != 1 and id !=2:
        response = {"status": "bad", "message": "Wrong player selected"}
        response = web.json_response(response)
        return response
    elif selectedSession.nextTurn != id:
        response = {"status": "bad", "message": "It is not your turn"}
        response = web.json_response(response)
        return response
    else:
        return None


@routes.get('/start')
async def gameStart(request):
    gameName = request.rel_url.query['name']
    newSession = session(gameName, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 1, -1)
    sessionArr.append(newSession)
    response = {"id": len(sessionArr)}
    response = web.json_response(response)
    return response

@routes.get('/status')
async def status(request):
        try:
            id = request.rel_url.query['game']
            id = int(id)
            if sessionArr[id-1] is not None:
                selectedSession = sessionArr[id-1]
            else:
                status = 400
                return web.Response(status=status)
        except:
            status = 400
            return web.Response(status=status)
        if int(selectedSession.winner) != -1: response = {"winner": int(selectedSession.winner)}
        else:
            response = {"board": selectedSession.playBoard, "next": int(selectedSession.nextTurn)}
        response = web.json_response(response)
        return response

@routes.get('/play')
async def play(request):
    try:
        id = request.rel_url.query['game']
        id = int(id)
        if sessionArr[id - 1] is not None:
            selectedSession = sessionArr[id - 1]
        else:
            status = 400
            return web.Response(status=status)
    except:
        status = 400
        return web.Response(status=status)

    if selectedSession.winner != -1:
        response = {"status": "bad", "message" : "Game is already ended"}
        response = web.json_response(response)
        return response

    try:
        player = request.rel_url.query['player']
        player = int(player)
        feed = checkPlayer(selectedSession, player)
        if feed is not None:
            return feed
    except:
        status = 400
        return web.Response(status=status)

#coords
    try:
        x = request.rel_url.query['x']
        x = int(x)
        y = request.rel_url.query['y']
        y = int(y)
    except:
        status = 400
        return web.Response(status=status)

    if (x > 2 or x < 0) or (y > 2 or y < 0):
        response = {"status": "bad", "message" : "Wrong coords entered"}
        response = web.json_response(response)
        return response

        # twice the same
    if selectedSession.playBoard[x][y] != 0:
            response = {"status": "bad", "message": "This turn was played before"}
            response = web.json_response(response)
            return response

# next turn
    if player == 1: sessionArr[id - 1].nextTurn = 2
    elif player == 2: sessionArr[id - 1].nextTurn = 1

# save
    sessionArr[id - 1].playBoard[x][y] = player

    finishedBool = isthereWinner(id, selectedSession, player)
    print(sessionArr[id - 1].winner)
    response = {"status": "OK"}
    response = web.json_response(response)
    return response

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=sys.argv[1])