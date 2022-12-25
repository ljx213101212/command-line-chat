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
        readCommand(text, client)
    elif cmd == C.CMD_REPLY:
        replyCommand(text, client)
    elif cmd == C.CMD_FORWARD:
        forwardCommand(text, client)
    elif cmd == C.CMD_BROADCAST:
        broadCastCommand(text, client)


def loginCommand(text, client):
    global clients
    global users
    lock = threading.Lock()

    with lock:
        if text not in users:
            users[text] = User(text, [])

        client.loggedInUser = users[text]
        client.client.send(
            str(getLoginMessage(client.loggedInUser)).encode(C.ENCODING_SCHEME))


def sendCommand(text, client):
    global clients
    global users
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
            len(users[target].messageThreads) + 1, client.loggedInUser, [client.loggedInUser], users[target], message))

        client.client.send(str(C.CMD_SEND_MESSAGE).encode(C.ENCODING_SCHEME))


def readCommand(text, client):
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

        idx = 0
        input = text.strip()
        readMessage = ""

        if input != "":
            try:
                idx = int(text) - 1
                if (idx == -1):
                    client.client.send(
                        str(C.CMD_READ_MESSAGE_CANCEL).encode(C.ENCODING_SCHEME))
                    return

                if (idx < 0 or idx >= len(messages)):
                    client.client.send(
                        str(C.CMD_READ_MESSAGE_OUT_OF_INDEX_ERROR).encode(C.ENCODING_SCHEME))
                    return
            except:
                client.client.send(
                    str(C.CMD_READ_MESSAGE_BAD_FORMAT_ERROR).encode(C.ENCODING_SCHEME))
                return

        readMessage = messages.pop(idx)
        client.currentMessage = readMessage
        client.client.send(str(getReadMessage(readMessage)
                               ).encode(C.ENCODING_SCHEME))


def replyCommand(text, client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        if not checkLoggedInGuard(client):
            return

        if client.currentMessage is None:
            client.client.send(
                (C.CMD_REPLY_MESSAGE_NO_TARGET).encode(C.ENCODING_SCHEME))
            return

        for currentMessageUser in client.currentMessage.sources:
            currentMessageUser.messageThreads.append(MessageThread(getMessageThreadId(currentMessageUser.messageThreads),
                                                                   client.loggedInUser, [client.loggedInUser],  currentMessageUser, text))

        client.client.send(
            (getReplyMessage(client.currentMessage.sources)).encode(C.ENCODING_SCHEME))


def forwardCommand(text, client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        if client.currentMessage is None:
            client.client.send(
                (C.CMD_REPLY_MESSAGE_NO_TARGET).encode(C.ENCODING_SCHEME))
            return
        if text not in users:
            users[text] = User(text, [])

        targetUser = users[text]
        client.currentMessage.sources.append(client.loggedInUser)
        targetUser.messageThreads.append(MessageThread(getMessageThreadId(
            targetUser.messageThreads), client.currentMessage.createdBy, client.currentMessage.sources, targetUser, client.currentMessage.message))

        client.client.send(
            (getForwardMessage(targetUser)).encode(C.ENCODING_SCHEME))


def broadCastCommand(text, client):
    global clients
    global users
    lock = threading.Lock()
    with lock:
        for username in users:
            users[username].messageThreads.append(MessageThread(getMessageThreadId(
                users[username].messageThreads), client.loggedInUser, [client.loggedInUser], users[username], text))


def checkLoggedInGuard(client):
    if client.loggedInUser is None:
        client.client.send(
            str(C.CMD_LOGIN_ERROR_MSSAGE).encode(C.ENCODING_SCHEME))
        return False

    return True


def getLoginMessage(loggedInUser):
    basic = f"{loggedInUser.name} logged in, {len(loggedInUser.messageThreads)} new messages."
    advance = f""
    if len(loggedInUser.messageThreads) > 1:
        advance = f"Choose a number from {1} to {len(loggedInUser.messageThreads)} to pick the message to read.Pick 0 to cancel."
    return str(basic + advance)


def getReadMessage(message):
    usersStr = ",".join([user.name for user in message.sources])
    basic = f"from {usersStr}: {message.message}"
    advance = f"message thread #{message.id}\n"
    return str(advance + basic)


def getMessageThreadId(messages):
    return len(messages) + 1


def getReplyMessage(targetUsers):
    usersStr = ",".join([user.name for user in targetUsers])
    return f"message sent to {usersStr}"


def getForwardMessage(targetUser):
    return f"message forwarded to {targetUser.name}"


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
                    f"id: {message.id} , createdBy: {message.createdBy.name}, target: {message.target.name}, message: {message.message}")
                for source in message.sources:
                    print(f"source: {source.name}")
