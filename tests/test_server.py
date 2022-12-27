import socket
from subprocess import Popen, PIPE
import threading
import unittest
from unittest.mock import patch
import src.constants as C
import src.command as COM
import src.utils as U
from src.models import User, MessageThread


def loginUser(self, user, numOfDummyMessage):
    U.send(self.client, f"{C.CMD_LOGIN} {user.name}")

    dummyUser = User(user.name, [MessageThread(
        0, user, user, user, "dummy message")] * numOfDummyMessage)
    self.assertEqual(U.receive(self.client),
                     U.getLoginMessage(dummyUser))


def sendMessageToUser(self, user, message):
    U.send(self.client, f"{C.CMD_SEND} {user.name} {message}")
    self.assertEqual(U.receive(self.client),
                     C.CMD_SEND_MESSAGE)

# Please start server before running this test suite
# python -m src.server


class Test_server(unittest.TestCase):

    client = None
    user1 = User("Jack")
    user2 = User("Rose")
    MSG = "Hello World!"
    user1ToUser2Message = MessageThread(1, user1, [user1], user2, MSG)
    user2ToUser1Message = MessageThread(1, user2, [user2], user1, MSG)

    def setUp(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((C.HOST, C.PORT))
        self.assertEqual(self.client.recv(
            C.MAX_MESSAGE_LENGTH).decode(), C.CMD_WELCOME)
        U.send(self.client, f"{C.CMD_LOGIN} {self.user1.name}")
        self.assertEqual(U.receive(self.client),
                         U.getLoginMessage(self.user1))

    def tearDown(self) -> None:
        U.send(self.client, f"{C.CMD_DEBUG} {C.CMD_DEBUG_TEXT_CLEAR}")
        self.client.close()

    def test_unknown_command(self):
        U.send(self.client, 'unknown command')
        self.assertEqual(U.receive(self.client),
                         C.CMD_UNKNOWN_COMMAND)

    # LOGIN
    def test_login_user_name_with_empty_name(self):
        U.send(self.client, C.CMD_LOGIN + "    ")
        self.assertEqual(U.receive(self.client),
                         C.CMD_LOGIN_USER_NAME_EMPTY_ERROR)

    def test_login_user_name(self):
        U.send(self.client, f"{C.CMD_LOGIN} {self.user1.name}")

        self.assertEqual(U.receive(self.client),
                         U.getLoginMessage(self.user1))

        U.send(self.client, f"{C.CMD_LOGIN} {self.user2.name}")
        self.assertEqual(U.receive(self.client),
                         U.getLoginMessage(self.user2))
    # SEND

    def test_send_to_current_logged_in_user(self):
        U.send(self.client, f"{C.CMD_SEND} {self.user1.name} {self.MSG}")
        self.assertEqual(U.receive(self.client),
                         C.CMD_SEND_MESSAGE_ERROR)

    def test_send_to_another_user_who_is_not_exist(self):
        U.send(self.client, f"{C.CMD_SEND} {self.user2.name} {self.MSG}")
        self.assertEqual(U.receive(self.client),
                         C.CMD_SEND_MESSAGE_USER_DOES_NOT_EXIST)

    def test_send_to_another_user_who_is_exist(self):
        loginUser(self, self.user2, 0)
        U.send(self.client, f"{C.CMD_SEND} {self.user1.name} {self.MSG}")
        self.assertEqual(U.receive(self.client),
                         C.CMD_SEND_MESSAGE)

    # READ

    def test_read_bad_format(self):
        lock = threading.Lock()

        with lock:
            loginUser(self, self.user2, 0)
            sendMessageToUser(self, self.user1, self.MSG)
            loginUser(self, self.user1, 1)
            U.send(self.client, f"{C.CMD_READ} !@#$%^&*()")
            self.assertEqual(U.receive(self.client),
                             C.CMD_READ_MESSAGE_BAD_FORMAT_ERROR)

    def test_read_out_of_index(self):
        loginUser(self, self.user2, 0)
        sendMessageToUser(self, self.user1, self.MSG)
        loginUser(self, self.user1, 1)

        U.send(self.client, f"{C.CMD_READ} {2}")
        self.assertEqual(U.receive(self.client),
                         C.CMD_READ_MESSAGE_OUT_OF_INDEX_ERROR)

    # REPLY
    def test_reply_without_read_message(self):
        loginUser(self, self.user2, 0)
        sendMessageToUser(self, self.user1, self.MSG)
        loginUser(self, self.user1, 1)
        U.send(self.client, f"{C.CMD_REPLY} {self.MSG}")
        self.assertEqual(U.receive(self.client),
                         C.CMD_REPLY_MESSAGE_NO_TARGET)

    def test_reply(self):
        loginUser(self, self.user2, 0)
        sendMessageToUser(self, self.user1, self.MSG)
        loginUser(self, self.user1, 1)
        U.send(self.client, f"{C.CMD_READ} 1")
        self.assertEqual(U.receive(self.client),
                         U.getReadMessage(self.user2ToUser1Message))
        U.send(self.client, f"{C.CMD_REPLY} {self.MSG}")
        self.assertEqual(U.receive(self.client),
                         U.getReplyMessage([User(self.user2.name, [])]))

    # FORWARD
    def test_forward_without_read_message(self):
        loginUser(self, self.user2, 0)
        sendMessageToUser(self, self.user1, self.MSG)
        loginUser(self, self.user1, 1)
        U.send(self.client, f"{C.CMD_FORWARD} {self.user2}")
        self.assertEqual(U.receive(self.client),
                         C.CMD_FORWARD_MESSAGE_NO_TARGET)

    def test_forward_current_login_user(self):
        loginUser(self, self.user2, 0)
        sendMessageToUser(self, self.user1, self.MSG)
        loginUser(self, self.user1, 1)
        U.send(self.client, f"{C.CMD_READ} 1")
        self.assertEqual(U.receive(self.client),
                         U.getReadMessage(self.user2ToUser1Message))
        U.send(self.client, f"{C.CMD_FORWARD} {self.user1.name}")
        self.assertEqual(U.receive(self.client),
                         C.CMD_FORWARD_MESSAGE_ERROR)

    def test_forward_to_user_who_is_not_exist(self):
        loginUser(self, self.user2, 0)
        sendMessageToUser(self, self.user1, self.MSG)
        loginUser(self, self.user1, 1)
        U.send(self.client, f"{C.CMD_READ} 1")
        self.assertEqual(U.receive(self.client),
                         U.getReadMessage(self.user2ToUser1Message))
        U.send(self.client, f"{C.CMD_FORWARD} someone_unknown")
        self.assertEqual(U.receive(self.client),
                         C.CMD_FORWARD_MESSAGE_USER_DOES_NOT_EXIST)

    def test_forward_to_user_who_is_exist(self):
        loginUser(self, self.user2, 0)
        sendMessageToUser(self, self.user1, self.MSG)
        loginUser(self, self.user1, 1)
        U.send(self.client, f"{C.CMD_READ} 1")
        self.assertEqual(U.receive(self.client),
                         U.getReadMessage(self.user2ToUser1Message))
        U.send(self.client, f"{C.CMD_FORWARD} {self.user2.name}")
        self.assertEqual(U.receive(self.client),
                         U.getForwardMessage(self.user2))

# BROADCAST
    def test_broadcast(self):
        loginUser(self, self.user2, 0)
        sendMessageToUser(self, self.user1, self.MSG)
        loginUser(self, self.user1, 1)
        U.send(self.client, f"{C.CMD_BROADCAST} {self.MSG}")
        loginUser(self, self.user2, 1)
        U.send(self.client, f"{C.CMD_READ} 1")
        self.assertEqual(U.receive(self.client),
                         U.getReadMessage(self.user1ToUser2Message))


if __name__ == '__main__':
    unittest.main()
