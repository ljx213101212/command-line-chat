import socket
import threading
import uuid
import traceback
import src.constants as C
from src.models import Client
import src.utils as U
import src.data as D

# socket initialization
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding host and port to socket
server.bind((C.HOST, C.PORT))
server.listen()


def broadcast(message):  # broadcast function declaration
    for client in D.clients:
        client.client.send(message)


def handle(client):
    while True:
        try:  # recieving valid messages from client
            message = client.client.recv(
                C.MAX_MESSAGE_LENGTH).decode(C.ENCODING_SCHEME)
            if len(message) == 0:
                raise Exception()

            cmdText = U.parseCommand(message)
            if (cmdText[0] == C.CMD_UNKNOWN):
                print("Unknown Command!")
                continue

            print(f"before do command {cmdText[0]}, {cmdText[1]}")
            U.doCommand(cmdText[0], cmdText[1], client)
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
        client.send(C.CMD_WELCOME.encode(C.ENCODING_SCHEME))
        clientObj = Client(uuid.uuid4(), client, None)
        D.clients.append(clientObj)
        thread = threading.Thread(target=handle, args=(clientObj,))
        thread.start()


if __name__ == "__main__":
    print("Start Server in {}".format(str(C.HOST) + ":" + str(C.PORT)))
    receive()

# broadcast("{} joined!".format(nickname).encode(C.ENCODING_SCHEME))
# client.send('Connected to server!'.encode(C.ENCODING_SCHEME))
# broadcast(message)
#
