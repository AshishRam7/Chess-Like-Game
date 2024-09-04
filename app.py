from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO,emit

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'chesslike'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

gameBoard = [[[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"]],[[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"]],[[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"]],[[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"]],[[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"],[-1,"None"]]]
player1 = True
player2 = True

def updateMove(player,pieceName,currPosX,currPosY,nextPosX,nextPosY):
    gameBoard[currPosX][currPosY][0] = -1
    gameBoard[currPosX][currPosY][1] = "None"

    gameBoard[nextPosX][nextPosY][0] = player
    gameBoard[nextPosX][nextPosY][1] = pieceName

def moveInvalid(player,stepCount,currPosX,currPosY,nextPosX,nextPosY):
    if(nextPosX not in range(0,5) or nextPosY not in range(0,5)):
        return True
    diffX = nextPosX - currPosX
    diffY = nextPosY - currPosY
    if((diffX not in range(stepCount-1,stepCount+1)) or (diffY not in range(stepCount-1,stepCount+1))):
        return True

    if(gameBoard[nextPosX][nextPosY][0] != -1 and gameBoard[nextPosX][nextPosY][0] == player):
        return True
    if(currPosX == nextPosX and currPosY == nextPosY):
        return True
    
    return False

@app.route("/player", methods = ['GET'])
def playerAvailable():
    global player1, player2
    if(player1 == True):
        player1 = False;
        return {"status":'success',
                "player": 1};
    if(player2 == True):
        player2 = False;
        return {"status":'success',
                "player": 2};
    else:
        return {"status":'failed'};

@app.route("/board" , methods = ['GET'])
def board():
    return gameBoard

@app.route("/move" , methods = ['POST'])
def move():
    data = request.get_json()
    player = data["piece"]
    pieceName = data["pieceName"]
    stepCount = data["step"]
    currPosX = data["current"][0]
    currPosY = data["current"][1]
    nextPosX = data["next"][0]
    nextPosY = data["next"][1]

    if(moveInvalid(player,stepCount,currPosX,currPosY,nextPosX,nextPosY)):
        print("Invalid Move")
        return {"status": 'invalid'}

    else:
        updateMove(player,pieceName,currPosX,currPosY,nextPosX,nextPosY)
        print(gameBoard[currPosX][currPosY])
        print(gameBoard[nextPosX][nextPosY])
        return {
            "status:": 'valid',
            "piece": [player,pieceName],
            "old": [currPosX , currPosY],
            "new": [nextPosX , nextPosY]
        }
    
@socketio.on("connect")
def connected():
    print(request.sid)
    print("client has connected")
    #emit("connect",{"data" :"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    print("data from the front end: ",str(data))
    if(len(data) == 4):
        player
    emit("data",{'data':data,'id':request.sid},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)


if __name__ == '__main__':
    # app.run()
    socketio.run(app,debug = True, port = 5001)
