import threading
import src.constants as C
from src.models import User, MessageThread
import src.data as D
import src.utils as U

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
    elif cmd == C.CMD_DEBUG:
        return (C.CMD_DEBUG, text)
    else:
        return (C.CMD_UNKNOWN, "")


def doCommand(cmd, text, client):
    if cmd == C.CMD_LOGIN:
        loginCommand(text, client)
    elif cmd == C.CMD_SEND:
        sendCommand(text, client)
    elif cmd == C.CMD_READ:
        readCommand(text, client)
    elif cmd == C.CMD_REPLY:
        replyCommand(text, client)
    elif cmd == C.CMD_FORWARD:
        forwardCommand(text, client)
    elif cmd == C.CMD_BROADCAST:
        broadCastCommand(text, client)
    elif cmd == C.CMD_DEBUG:
        debugCommand(text, client)


def loginCommand(text, client):
    global clients
    global users
    lock = threading.Lock()

    with lock:
        username = text.strip()
        if len(username) == 0:
            U.send(client.client, C.CMD_LOGIN_USER_NAME_EMPTY_ERROR)
            return
        if username not in users:
            users[username] = User(username, [])

        client.loggedInUser = users[username]
        U.send(client.client, U.getLoginMessage(client.loggedInUser))


def sendCommand(text, client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        if not U.checkLoggedInGuard(client):
            return
        targetMessageTurple = text.split(maxsplit=1)

        if len(targetMessageTurple) < 2:
            U.send(client.client, C.CMD_SEND_MESSAGE_NO_TARGET)
            return

        target = targetMessageTurple[0]
        message = targetMessageTurple[1]

        if client.loggedInUser.name == target:
            U.send(client.client, C.CMD_SEND_MESSAGE_ERROR)
            return

        if target not in users:
            U.send(client.client, C.CMD_SEND_MESSAGE_USER_DOES_NOT_EXIST)
            return

        users[target].messageThreads.append(MessageThread(
            len(users[target].messageThreads) + 1, client.loggedInUser, [client.loggedInUser], users[target], message))

        U.send(client.client, C.CMD_SEND_MESSAGE)


def readCommand(text, client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        if not U.checkLoggedInGuard(client):
            return

        messages = users[client.loggedInUser.name].messageThreads
        if len(messages) == 0:
            U.send(client.client, C.CMD_READ_MESSAGE_EMPTY)
            return

        idx = 0
        input = text.strip()
        readMessage = ""

        if input != "":
            try:
                idx = int(text) - 1
                if (idx == -1):
                    U.send(client.client, C.CMD_READ_MESSAGE_CANCEL)
                    return

                if (idx < 0 or idx >= len(messages)):
                    U.send(client.client, C.CMD_READ_MESSAGE_OUT_OF_INDEX_ERROR)
                    return
            except:
                U.send(client.client, C.CMD_READ_MESSAGE_BAD_FORMAT_ERROR)
                return

        readMessage = messages.pop(idx)
        client.currentMessage = readMessage
        U.send(client.client, U.getReadMessage(readMessage))


def replyCommand(text, client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        if not U.checkLoggedInGuard(client):
            return

        if client.currentMessage is None:
            U.send(client.client, C.CMD_REPLY_MESSAGE_NO_TARGET)
            return

        for currentMessageUser in client.currentMessage.sources:
            currentMessageUser.messageThreads.append(MessageThread(U.getMessageThreadId(currentMessageUser.messageThreads),
                                                                   client.loggedInUser, [client.loggedInUser],  currentMessageUser, text))

        U.send(client.client, U.getReplyMessage(client.currentMessage.sources))


def forwardCommand(text, client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        if not U.checkLoggedInGuard(client):
            return
        if client.currentMessage is None:
            U.send(client.client, C.CMD_REPLY_MESSAGE_NO_TARGET)
            return

        username = text.strip()
        if client.loggedInUser.name == username:
            U.send(client.client, C.CMD_FORWARD_MESSAGE_ERROR)
            return
        if username not in users:
            U.send(client.client, C.CMD_FORWARD_MESSAGE_USER_DOES_NOT_EXIST)
            return

        targetUser = users[username]
        client.currentMessage.sources.append(client.loggedInUser)
        targetUser.messageThreads.append(MessageThread(U.getMessageThreadId(
            targetUser.messageThreads), client.currentMessage.createdBy, client.currentMessage.sources, targetUser, client.currentMessage.message))

        U.send(client.client, U.getForwardMessage(targetUser))


def broadCastCommand(text, client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        if not U.checkLoggedInGuard(client):
            return
        for username in users:
            users[username].messageThreads.append(MessageThread(U.getMessageThreadId(
                users[username].messageThreads), client.loggedInUser, [client.loggedInUser], users[username], text))


def debugCommand(text, client):
    if text == C.CMD_DEBUG_TEXT_CLEAR:
        debugClear()
    elif text == C.CMD_DEBUG_TEXT_PRINT:
        debugPrint()


def debugPrint():
    U.printUsers()


def debugClear():
    global users
    users.clear()
