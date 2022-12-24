import socket
import threading
import src.constants as C
import src.utils as U

# socket initialization
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connecting client to server
client.connect((C.HOST, C.PORT))


def receive():
    # making valid connection
    while True:
        try:
            message = client.recv(
                C.MAX_MESSAGE_LENGTH).decode(C.ENCODING_SCHEME)
            if len(message) == 0:
                raise Exception("message is empty")
            print(message)
        # case on wrong ip/port details
        except:
            print("An error occured!")
            client.close()
            break


def write():
    # message layout
    while True:
        inputCommand = input('')
        cmdText = U.parseCommand(inputCommand)

        if (cmdText[0] == C.CMD_UNKNOWN):
            print("Unknown Command!")
            continue
        client.send(inputCommand.encode('ascii'))


# receiving multiple messages
receive_thread = threading.Thread(
    target=receive)
receive_thread.start()

# sending messages
write_thread = threading.Thread(target=write)
write_thread.start()
