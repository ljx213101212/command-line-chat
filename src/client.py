import socket
import threading
nickname = input("Choose your nickname: ")

# socket initialization
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connecting client to server
client.connect(('127.0.0.1', 7976))


def receive():
    # making valid connection
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print('received:' + message)
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        # case on wrong ip/port details
        except:
            print("An error occured!")
            client.close()
            break


def write():
    # message layout
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


# receiving multiple messages
receive_thread = threading.Thread(
    target=receive)
receive_thread.start()

# sending messages
write_thread = threading.Thread(target=write)
write_thread.start()
