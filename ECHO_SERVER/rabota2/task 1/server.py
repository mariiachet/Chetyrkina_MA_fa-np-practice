import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(0)

while True:
    conn, addr = sock.accept()
    print(addr)

    msg = ''

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg += data.decode()
            conn.send(data)

    except ConnectionError:
        print("Connection error. Client disconnected.")
        conn.close()

    print(msg)

    conn.close()