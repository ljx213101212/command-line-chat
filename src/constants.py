HOST = '127.0.0.1'  # LocalHost
PORT = 7977  # Choosing unreserved port
ENCODING_SCHEME = 'ascii'
MAX_MESSAGE_LENGTH = 1024


CMD_WELCOME = 'WELCOME'
CMD_LOGIN = 'LOGIN'
CMD_SEND = 'SEND'
CMD_READ = 'READ'
CMD_REPLY = 'REPLY'
CMD_FORWARD = 'FORWARD'
CMD_BROADCAST = 'BROADCAST'
CMD_UNKNOWN = 'UNKNOWN'


CMD_LOGIN_SUCCESS_MESSAGE = 'logged in.'
CMD_LOGIN_ERROR_MSSAGE = 'error: please login first.'
CMD_SEND_MESSAGE = 'message sent.'
CMD_SEND_MESSAGE_ERROR = 'error: cannot send a message to logged in user.'
CMD_READ_MESSAGE_EMPTY = 'Empty message.'
CMD_REPLY_MESSAGE_NO_TARGET = 'error: please read a message first.'
