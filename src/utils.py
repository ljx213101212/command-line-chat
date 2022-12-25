import threading
import src.constants as C


def send(client, message):
    client.send(message.encode(C.ENCODING_SCHEME))


def checkLoggedInGuard(client):
    if client.loggedInUser is None:
        send(client.client, C.CMD_LOGIN_ERROR_MSSAGE)
        return False

    return True


def checkIsKnownCommand(cmd):
    if cmd == C.CMD_UNKNOWN:
        print("Unknown Command!")
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


# For debug purpose only
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
