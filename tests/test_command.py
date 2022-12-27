import unittest
from unittest.mock import Mock, patch
import src.constants as C
import src.command as COM
import src.utils as U
from src.models import User, MessageThread


class Test_parse_command(unittest.TestCase):

    def tearDown(self) -> None:
        COM.debugClear()

    def test_parse_command_special_characters(self):
        cmd, _text = COM.parseCommand(" ~!@#$%^&*()_ +")
        self.assertEqual(cmd,
                         C.CMD_UNKNOWN)

    def test_parse_command_empty_space(self):
        cmd, _text = COM.parseCommand("   ")
        self.assertEqual(cmd,
                         C.CMD_UNKNOWN)

    def test_parse_command_login(self):
        username = "ajdslkaklsdjkl"
        cmd, text = COM.parseCommand(f"   {C.CMD_LOGIN}  {username}")
        self.assertEqual(cmd,
                         C.CMD_LOGIN)
        self.assertEqual(text, username)

    def test_parse_command_send(self):
        username = "ajdslkaklsdjkl"
        message = "   "
        cmd, text = COM.parseCommand(f"   {C.CMD_SEND}  {username} {message}")
        self.assertEqual(cmd,
                         C.CMD_SEND)
        self.assertEqual(text, f"{username} {message}")

    def test_parse_command_send(self):
        username = "ajdslkaklsdjkl"
        message = "   "
        cmd, text = COM.parseCommand(f"   {C.CMD_SEND}  {username} {message}")
        self.assertEqual(cmd,
                         C.CMD_SEND)
        self.assertEqual(text, f"{username} {message}")

    def test_parse_command_read(self):
        cmd, text = COM.parseCommand(f"{C.CMD_READ} {1}")
        self.assertEqual(cmd,
                         C.CMD_READ)
        self.assertEqual(text, f"{1}")

    def test_parse_command_reply(self):
        message = "this is a reply"
        cmd, text = COM.parseCommand(f"{C.CMD_REPLY} {message}")
        self.assertEqual(cmd,
                         C.CMD_REPLY)
        self.assertEqual(text, message)

    def test_parse_command_forward(self):
        username = "this is username"
        cmd, text = COM.parseCommand(f"{C.CMD_FORWARD} {username}")
        self.assertEqual(cmd,
                         C.CMD_FORWARD)
        self.assertEqual(text, username)

    def test_parse_command_broadcast(self):
        message = "this is a broadcast message"
        cmd, text = COM.parseCommand(f"{C.CMD_BROADCAST} {message}")
        self.assertEqual(cmd,
                         C.CMD_BROADCAST)
        self.assertEqual(text, message)


class Test_do_command(unittest.TestCase):

    def tearDown(self) -> None:
        COM.debugClear()

    def test_do_login_command_without_username(self):
        clientMock = Mock()
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "", clientMock)
        U.send.assert_called_once_with(
            clientMock.client, C.CMD_LOGIN_USER_NAME_EMPTY_ERROR)

    def test_do_login_command(self):
        clientMock = Mock()
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "jack", clientMock)
        U.send.assert_called_once_with(
            clientMock.client, U.getLoginMessage(User("jack", [])))

    def test_do_send_command_without_login(self):
        message = "jack message to jack"
        client = Mock()
        client.client = Mock()
        client.loggedInUser = None
        U.send = Mock()
        COM.doCommand(C.CMD_SEND, message, client)
        U.send.assert_called_once_with(
            client.client, C.CMD_LOGIN_ERROR_MSSAGE)

    def test_do_send_command_to_current_loggedInUser(self):
        message = "rose message to rose"
        client = Mock()
        client.client = Mock()
        client.loggedInUser = User("rose")
        U.send = Mock()
        COM.doCommand(C.CMD_SEND, message, client)
        U.send.assert_called_once_with(
            client.client, C.CMD_SEND_MESSAGE_ERROR)

    def test_do_send_command_to_empty_user(self):
        message = ""
        client = Mock()
        client.client = Mock()
        client.loggedInUser = User("rose")
        U.send = Mock()
        COM.doCommand(C.CMD_SEND, message, client)
        U.send.assert_called_once_with(
            client.client, C.CMD_SEND_MESSAGE_NO_TARGET)

    def test_do_send_command(self):
        message = "rose message to rose"
        client = Mock()
        client.client = Mock()
        client.loggedInUser = User("jack")
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_SEND, message, client)
        U.send.assert_called_with(
            client.client, C.CMD_SEND_MESSAGE)

    def test_do_read_command_out_of_index(self):
        client = Mock()
        client.client = Mock()
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_SEND, "jack hello", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_READ, "2", client)
        U.send.assert_called_with(
            client.client, C.CMD_READ_MESSAGE_OUT_OF_INDEX_ERROR)

    def test_do_read_command(self):
        client = Mock()
        client.client = Mock()
        client.loggedInUser = User("Jack", [MessageThread(
            1, User("rose"), [User("rose")], User("jack"), "hello")])
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_SEND, "jack hello", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_READ, "", client)
        U.send.assert_called_with(
            client.client, U.getReadMessage(MessageThread(
                1, User("rose"), [User("rose")], User("jack"), "hello")))

    def test_do_reply_command_without_reading_current_message(self):
        client = Mock()
        client.client = Mock()
        client.currentMessage = None
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_SEND, "jack hello", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_REPLY, "world", client)
        U.send.assert_called_with(
            client.client, C.CMD_REPLY_MESSAGE_NO_TARGET)

    def test_do_reply_command(self):
        client = Mock()
        client.client = Mock()
        client.currentMessage = MessageThread(
            1, User("rose"), [User("rose")], User("jack"), "hello")
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_SEND, "jack hello", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_READ, "", client)
        COM.doCommand(C.CMD_REPLY, "world", client)
        U.send.assert_called_with(
            client.client, U.getReplyMessage([User("rose", [])]))

    def test_do_forward_command_without_reading_current_message(self):
        client = Mock()
        client.client = Mock()
        client.currentMessage = None
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_SEND, "jack hello", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_FORWARD, "rose", client)
        U.send.assert_called_with(
            client.client, C.CMD_FORWARD_MESSAGE_NO_TARGET)

    def test_do_forward_command_to_current_login_user(self):
        client = Mock()
        client.client = Mock()
        client.currentMessage = MessageThread(
            1, User("rose"), [User("rose")], User("jack"), "hello")
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_SEND, "jack hello", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_READ, "", client)
        COM.doCommand(C.CMD_FORWARD, "jack", client)
        U.send.assert_called_with(
            client.client, C.CMD_FORWARD_MESSAGE_ERROR)

    def test_do_forward_command(self):
        client = Mock()
        client.client = Mock()
        client.currentMessage = MessageThread(
            1, User("rose"), [User("rose")], User("jack"), "hello")
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_SEND, "jack hello", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_READ, "", client)
        COM.doCommand(C.CMD_FORWARD, "rose", client)
        U.send.assert_called_with(
            client.client, U.getForwardMessage(User("rose", [])))

    def test_do_broadcast_command(self):
        client = Mock()
        client.client = Mock()
        client.currentMessage = None
        U.send = Mock()
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_LOGIN, "captain", client)
        COM.doCommand(C.CMD_LOGIN, "iceberg", client)
        COM.doCommand(C.CMD_BROADCAST, "warning", client)
        COM.doCommand(C.CMD_READ, "", client)
        U.send.assert_called_with(
            client.client, U.getReadMessage(MessageThread(1, User("iceberg"), [User("iceberg")], User("iceberg"), "warning")))
        COM.doCommand(C.CMD_LOGIN, "captain", client)
        COM.doCommand(C.CMD_READ, "", client)
        U.send.assert_called_with(
            client.client, U.getReadMessage(MessageThread(1, User("iceberg"), [User("iceberg")], User("captain"), "warning")))
        COM.doCommand(C.CMD_LOGIN, "jack", client)
        COM.doCommand(C.CMD_READ, "", client)
        U.send.assert_called_with(
            client.client, U.getReadMessage(MessageThread(1, User("iceberg"), [User("iceberg")], User("jack"), "warning")))
        COM.doCommand(C.CMD_LOGIN, "rose", client)
        COM.doCommand(C.CMD_READ, "", client)
        U.send.assert_called_with(
            client.client, U.getReadMessage(MessageThread(1, User("iceberg"), [User("iceberg")], User("rose"), "warning")))
