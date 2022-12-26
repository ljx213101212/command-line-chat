import socket
from subprocess import Popen, PIPE
import threading
import unittest
from unittest.mock import patch
import src.constants as C
import src.command as COM
import src.utils as U
from src.models import User, MessageThread
import src.data as D


clients = D.clients
users = D.users


# Please start server before running this test suite
# python -m src.server
class Test_server(unittest.TestCase):

    client = None
    user1 = User("Jack")
    user2 = User("Rose")

    def setUp(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((C.HOST, C.PORT))
        self.assertEqual(self.client.recv(
            C.MAX_MESSAGE_LENGTH).decode(), C.CMD_WELCOME)

    def tearDown(self) -> None:
        self.client.close()

    def test_unknown_command(self):
        U.send(self.client, 'unknown command')
        self.assertEqual(U.receive(self.client),
                         C.CMD_SEND_MESSAGE_UNKNOWN)

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


if __name__ == '__main__':
    unittest.main()
