class Client:
    def __init__(self, id, client=None, loggedInUser=None):
        self.id = id
        self.client = client
        self.loggedInUser = loggedInUser


class User:
    def __init__(self, name="", messageThreads=[]):
        self.name = name
        self.messageThreads = messageThreads


class MessageThread:
    def __init__(self, id, createdBy, source, target, message):
        self.id = id
        self.createdBy = createdBy
        self.source = source
        self.target = target
        self.message = message
