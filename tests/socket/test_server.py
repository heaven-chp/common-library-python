import random
from common_library import socket


def test_start():

    def serverJob(client):
        client.send(bytes("greeting\r\n", 'utf-8'))
        data = client.recv(1024).decode('utf-8')
        client.send(bytes("[response] : " + data, 'utf-8'))
        client.close()

    port = random.randrange(10000, 15000)

    server = socket.Server()

    server.start(address='0.0.0.0',
                 port=port,
                 listen_size=10,
                 serverJob=serverJob)

    client = socket.Client()
    client.close()
    client.conenct(address='127.0.0.1', port=port, timeout=3)

    data = client.recv()
    assert data == "greeting\r\n"

    send_len = client.send("data\r\n")
    assert send_len == 6

    data = client.recv()
    assert data == "[response] : data\r\n"

    client.close()

    server.stop()


def test_stop():
    server = socket.Server()
    server.stop()
