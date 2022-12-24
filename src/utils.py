import threading
import src.constants as C
from src.models import User, MessageThread
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
        sendCommand(text, client)
    elif cmd == C.CMD_READ:
        readCommand(client)
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


def sendCommand(text, client):
    lock = threading.Lock()
    with lock:
        if not checkLoggedInGuard(client):
            return
        targetMessageTurple = text.split(maxsplit=1)
        target = targetMessageTurple[0]
        message = targetMessageTurple[1]

        if client.loggedInUser.name == target:
            client.client.send(
                str(C.CMD_SEND_MESSAGE_ERROR).encode(C.ENCODING_SCHEME))
            return

        if target not in users:
            users[target] = User(target, [])

        users[target].messageThreads.append(MessageThread(
            len(users[target].messageThreads) + 1, client.loggedInUser, client.loggedInUser, users[target], message))

        client.client.send(str(C.CMD_SEND_MESSAGE).encode(C.ENCODING_SCHEME))

    print("TODO: sendCommand")


def readCommand(client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        if not checkLoggedInGuard(client):
            return

        messages = users[client.loggedInUser.name].messageThreads
        if len(messages) == 0:
            client.client.send(
                str(C.CMD_READ_MESSAGE_EMPTY).encode(C.ENCODING_SCHEME))
            return

        readMessage = messages.pop(0)

        client.client.send(str(getReadMessage(readMessage)
                               ).encode(C.ENCODING_SCHEME))

    print("TODO: readCommand")


def replyCommand(text):
    print("TODO: replyCommand")


def forwardCommand(text):
    print("TODO: forwardCommand")


def broadCastCommand(text):
    print("TODO: broadCastCommand")


def checkLoggedInGuard(client):
    if client.loggedInUser is None:
        client.client.send(
            str(C.CMD_LOGIN_ERROR_MSSAGE).encode(C.ENCODING_SCHEME))
        return False

    return True


def getReadMessage(message):
    return f"from {message.source.name}: {message.message}"


def printUsers():
    global clients
    global users

    lock = threading.Lock()
    with lock:
        for key in users:
            print(f"user -> {users[key].name}")
            # print(f"{users[key].messageThreads}")
            threads = users[key].messageThreads
            for message in threads:
                print(
                    f"id: {message.id} , createdBy: {message.createdBy.name}, source: {message.source.name}, target: {message.target.name}, message: {message.message}")
