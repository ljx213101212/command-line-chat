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

CMD_DEBUG = 'DEBUG'
CMD_DEBUG_TEXT_CLEAR = 'clear'
CMD_DEBUG_TEXT_PRINT = 'print'


CMD_UNKNOWN_COMMAND = 'error: unknown command.'
CMD_LOGIN_SUCCESS_MESSAGE = 'logged in.'
CMD_LOGIN_ERROR_MSSAGE = 'error: please login first.'
CMD_LOGIN_USER_NAME_EMPTY_ERROR = 'error: username cannot be empty'
CMD_SEND_MESSAGE = 'message sent.'
CMD_SEND_MESSAGE_ERROR = 'error: cannot send a message to current user.'
CMD_SEND_MESSAGE_NO_TARGET = 'error: cannot send a message without a target or message.'
CMD_SEND_MESSAGE_USER_DOES_NOT_EXIST = 'error: cannot send a message to a user who does not exist.'
CMD_READ_MESSAGE_EMPTY = 'Empty message.'
CMD_READ_MESSAGE_OUT_OF_INDEX_ERROR = 'error: out of message thread index.'
CMD_READ_MESSAGE_BAD_FORMAT_ERROR = 'error: read command receive number only.'
CMD_READ_MESSAGE_CANCEL = 'Message reading cancelled.'
CMD_REPLY_MESSAGE_NO_TARGET = 'error: please read a message first.'
CMD_FORWARD_MESSAGE_NO_TARGET = 'error: please read a message first.'
CMD_FORWARD_MESSAGE_ERROR = 'error: cannot forward a message to current user. '
CMD_FORWARD_MESSAGE_USER_DOES_NOT_EXIST = 'error: cannot forward a message to a user who does not exist.'
