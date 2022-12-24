class Client:
    def __init__(self, id, client=None, loggedInUser=None, currentMessage=None):
        self.id = id
        self.client = client
        self.loggedInUser = loggedInUser
        self.currentMessage = currentMessage


class User:
    def __init__(self, name="", messageThreads=[]):
        self.name = name
        self.messageThreads = messageThreads


class MessageThread:
    def __init__(self, id, createdBy, sources, target, message):
        self.id = id
        self.createdBy = createdBy
        self.sources = sources
        self.target = target
        self.message = message
