import threading
import src.constants as C
from src.models import User
# import src.server
import src.data as D

clients = D.clients
users = D.users


def parseCommand(command):
    cmds = command.split(maxsplit=1)

    if len(cmds) == 0:
        return (C.CMD_UNKNOWN, "")

    cmd = cmds[0].upper()
    text = "" if len(cmds) <= 1 else cmds[1]

    if cmd == C.CMD_LOGIN:
        return (C.CMD_LOGIN, text)
    elif cmd == C.CMD_SEND:
        return (C.CMD_SEND, text)
    elif cmd == C.CMD_READ:
        return (C.CMD_READ, text)
    elif cmd == C.CMD_REPLY:
        return (C.CMD_REPLY, text)
    elif cmd == C.CMD_FORWARD:
        return (C.CMD_FORWARD, text)
    elif cmd == C.CMD_BROADCAST:
        return (C.CMD_BROADCAST, text)
    else:
        return (C.CMD_UNKNOWN, "")


def doCommand(cmd, text, client):
    if cmd == C.CMD_LOGIN:
        loginCommand(text, client)
    elif cmd == C.CMD_SEND:
        sendCommand(text)
    elif cmd == C.CMD_READ:
        readCommand(text)
    elif cmd == C.CMD_REPLY:
        replyCommand(text)
    elif cmd == C.CMD_FORWARD:
        forwardCommand(text)
    elif cmd == C.CMD_BROADCAST:
        broadCastCommand(text)


def loginCommand(text, client):
    print(f"TODO: loginCommand start {text}")
    global clients
    global users
    lock = threading.Lock()

    with lock:
        if text not in users:
            users[text] = User(text, [])

        client.loggedInUser = users[text]
        client.client.send(str(client.loggedInUser.name + " " +
                           C.CMD_LOGIN_SUCCESS_MESSAGE).encode(C.ENCODING_SCHEME))

    print(f"TODO: loginCommand {text}")


def sendCommand(text):
    print("TODO: sendCommand")


def readCommand(text):
    print("TODO: readCommand")


def replyCommand(text):
    print("TODO: replyCommand")


def forwardCommand(text):
    print("TODO: forwardCommand")


def broadCastCommand(text):
    print("TODO: broadCastCommand")
