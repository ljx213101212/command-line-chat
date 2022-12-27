import socket
import threading
import uuid
import traceback
import src.constants as C
import src.data as D
import src.command as COM
import src.utils as U
from src.models import Client

# socket initialization
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding host and port to socket
server.bind((C.HOST, C.PORT))
server.listen()


def handle(client):
    while True:
        try:  # recieving valid messages from client
            message = client.client.recv(
                C.MAX_MESSAGE_LENGTH).decode(C.ENCODING_SCHEME)
            if len(message) == 0:
                continue

            cmd, text = COM.parseCommand(message)
            if not U.checkIsKnownCommand(cmd):
                U.send(client.client, C.CMD_UNKNOWN_COMMAND)
                continue
            # print(f"before do command {cmd}, {text}")
            COM.doCommand(cmd, text, client)
            # U.printUsers()

        except Exception as e:  # removing clients
            print(traceback.format_exc())
            index = next((i for i, cli in enumerate(
                D.clients) if cli.id == client.id), -1)
            if index >= 0:
                D.clients.pop()
            client.client.close()
            break


def receive():  # accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        U.send(client, C.CMD_WELCOME)
        clientObj = Client(uuid.uuid4(), client, None)
        D.clients.append(clientObj)
        thread = threading.Thread(target=handle, args=(clientObj,))
        thread.start()


if __name__ == "__main__":
    print("Start Server in {}".format(str(C.HOST) + ":" + str(C.PORT)))
    receive()
