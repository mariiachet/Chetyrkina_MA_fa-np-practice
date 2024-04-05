import socket
import hashlib

def get_client_name(ip_address):
    with open("clients.txt", "r") as file:
        for line in file:
            client_ip, client_name, password = line.strip().split(':')
            if client_ip == ip_address:
                return client_name, password
    return None
def hash(client_name, password):
    password = client_name[0] + password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def save_client_name(ip_address, client_name, password):
    with open("clients.txt", "a") as file:
        password = hash(client_name, password)
        file.write(f"{ip_address}:{client_name}:{password}\n")

sock = socket.socket()
sock.bind(('127.0.0.1', 9090))
sock.listen(0)
conn, addr = sock.accept()
print(addr)

client_ip = addr[0]
try:
    client_name, password = get_client_name(client_ip)
    conn.send(f"Welcome back, {client_name}! Enter your password: ".encode())
    entered_password = conn.recv(1024).decode().strip()
    if password == hash(client_name, entered_password):
        conn.send(f"Welcome back, {client_name}! Your password is right ".encode())
except TypeError:
    conn.send("Please enter your name and password, like name;password: ".encode())
    client_name, password = conn.recv(1024).decode().split(";")
    save_client_name(client_ip.strip(), client_name.strip(), password.strip())
    conn.send("Your name has been saved. Welcome!".encode())
conn.close()