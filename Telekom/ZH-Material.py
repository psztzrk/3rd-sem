################    Basic client    ################
import socket
import sys

server_addr = (sys.argv[1], int(sys.argv[2]))   # place, port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(server_addr)
    client.sendall("Hello server".encode())
    data = client.recv(16)
    print("Received:", data.decode())

################    Basic server    ################
import socket
import sys

server_addr = ("localhost", int(sys.argv[1]))   # port  - (server, port) 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_addr)
    sock.listen(1)
    sock.settimeout(1.0) # Windowson a Ctrl+C csak igy szakitja meg az accept-et

    try:
        while True:
            try:
                client, client_addr = sock.accept()
                with client:
                    print("Connected:", client_addr)
                    data = client.recv(16)
                    print("Received:", data.decode())
                    client.sendall("Hello client".encode())
            except TimeoutError:
                pass
    except KeyboardInterrupt:
        print("Server stopped")

################    Select client    ################
import socket
import struct

ADDR = ("localhost", 10000)
packer = struct.Struct("i i c")

with socket.create_connection(ADDR) as sock:
    sock.sendall(b"Hello server")
    print("Válasz:", sock.recv(1024))

################    Select server    ################
import select
import socket
import struct

ADDR = ("localhost", 10000)
packer = struct.Struct("i i c")

def recv_exact(sock, size):
    """Addig olvas, amíg pontosan size byte meg nem érkezik (vagy a másik oldal bont)."""
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data

"""Egyszerre több klienssel foglalkozik: a select megmondja, melyik socketen van teendő."""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(ADDR)
    server.listen(5)
    print("Select szerver fut:", ADDR)
    inputs = [server]
    while True:
        readables, _, _ = select.select(inputs, [], [], 1.0)
        for s in readables:
            if s is server:  # új kliens csatlakozik, a szerver csak idáig megy a continue miatt
                client, addr = server.accept()
                inputs.append(client)
                print("Új kliens:", addr)
                continue
            msg = recv_exact(s, packer.size)
            if not msg:  # b"" -> a kliens bontotta a kapcsolatot
                print("Egy kliens bontott")
                s.close()
                inputs.remove(s)
                continue
            print(f"{s.getpeername()}: {msg!r} ({len(msg)} byte)")
            print("Kicsomagolva:", packer.unpack(msg))
            s.sendall(b"OK")

################    Blocking server    ################ (client is same as "select client")
import socket
import time

ADDR = ("localhost", 10000)

"""Egyszerre egy klienssel foglalkozik: accept -> recv -> válasz -> bontás."""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen(0)  # a lehető legrövidebb várakozási sor (nagyobbítani)
    print("Blokkoló szerver fut:", ADDR)
    while True:
        client, addr = server.accept()
        with client:
            msg = client.recv(1024)
            print(f"{addr}: {msg!r}")
            time.sleep(2)  # lassú kiszolgálás, hogy lássuk a sorban állást (törölni)
            client.sendall(b"Hello client")
            client.recv(1024)  # megvárjuk, hogy a kliens bontson: így a port újraindításkor szabad

################    UDP client    ################
import socket
import time

ADDR = ("localhost", 10001)

"""egy datagram a szervernek, majd várjuk a választ."""
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sent = sock.sendto(b"Hello server!", ADDR)
    print(f"Sent {sent} bytes, waiting for a response...")
    data, server = sock.recvfrom(1024)
    print(f"Response from {server}: {data!r}")

################    UDP server    ################
import socket

ADDR = ("localhost", 10001)

"""UDP szerver: nincs listen, accept; minden datagram a feladó címével együtt érkezik."""
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(ADDR)
    print("UDP server is running:", ADDR)
    while True:
        data, client = sock.recvfrom(1024)
        print(f"{client}: {data!r} ({len(data)} byte)")
        sock.sendto(b"Hello client", client)

################    Proxy server    ################
import select
import socket
import struct

PROXY_ADDR = ("localhost", 10000)
SERVER_ADDR = ("localhost", 10002)  # a square_server.py

in_packer = struct.Struct("10s i")  # a klienstol: nev es szam
out_packer = struct.Struct("i")  # a szervernek: csak a szam; a szerver valasza is (i)
reply_packer = struct.Struct("10s i")  # a kliensnek: a nev es a szerver valasza

"""A kliensek felé szerver (select), a szerver felé kliens: egyetlen, állandó kapcsolattal."""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend, socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
) as server:
    backend.connect(SERVER_ADDR)  # egyszer, a ciklus elott
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(PROXY_ADDR)
    server.listen(5)
    print("Proxy is running:", PROXY_ADDR, "->", SERVER_ADDR)
    inputs = [server]  # a backend NEM kerul ide: a valaszt rogton megvarjuk rajta
    while True:
        readables, _, _ = select.select(inputs, [], [], 1.0)
        for s in readables:
            if s is server:
                client, addr = server.accept()
                print(f"New client: {addr[0]}:{addr[1]}")
                inputs.append(client)
                continue
            msg = recv_exact(s, in_packer.size)
            if not msg:
                inputs.remove(s)
                s.close()
                continue
            # atcsomagolas: a szerver csak a szamot kapja
            name, n = in_packer.unpack(msg)
            backend.sendall(out_packer.pack(n))
            (result,) = out_packer.unpack(recv_exact(backend, out_packer.size))
            shown = name.rstrip(b"\x00").decode()
            print(f"{shown}: {n} -> server -> {result}")
            s.sendall(reply_packer.pack(name, result))

################    Server with buffer (no holdup)    ################
def read_full(sock, buffer):
    chunk = sock.recv(512)
    if not chunk:
        return b""
    buffer[sock].extend(chunk)
    if b"\r\n\r\n" not in buffer[sock]: # arguement on what to check for
        return None
    data = bytes(buffer.pop(sock))
    return data

"""Egyszerre több klienssel foglalkozik: a select megmondja, melyik socketen van teendő."""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(5)
    inputs = [server]
    client_buffers = {}
    while True:
        readables, _, _ = select.select(inputs, [], [], 1.0)
        for s in readables:
            if s is server:
                client, addr = server.accept()
                inputs.append(client)
                client_buffers[client] = bytearray()
                continue
            data = read_full(s, client_buffers)
            if data is None:
                continue
            if not data:
                s.close()
                inputs.remove(s)
                continue

################    Misc.    ################
ip, port = socket.getpeername() # getpeername() gives back the client's ip and port in a touple
hostname = socket.gethostname() # gethostname() gives bak the hosts name
ip = socket.gethostbyname('www.example.org') # gethostbyname() takes a name and gives back it's ip
hostname, aliases, addresses = socket.gethostbyname_ex(host)
hostname, aliases, addresses = socket.gethostbyaddr('157.181.161.79')

inputs = [ server ]
outputs = [ ]
timeout=1
readable, writable, exceptional = select.select(inputs, outputs, inputs,timeout)    # Select full example (most unused, check select server for more accuracy)

def recv_exact(sock, size):
    """Addig olvas, amíg pontosan size byte meg nem érkezik (vagy a másik oldal bont)."""
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data

#   Byte orders
#   @/=   =   native
#   <     =   little-endian
#   >     =   big-endian
#   !     =   network(=big-endian)

#   Format    *  C Type    *      Python type    *    Size
#   x            pad byte         no value
#   c            char             bytes len:1         1
#   b            signed char      integer             1
#   B            unsigned char    integer             1
#   ?            _Bool            bool                1
#   h            short            integer             2
#   H            unsigned short   integer             2
#   i            int              integer             4
#   I            uns. int         integer             4
#   f            float            float               4
#   d            double           float               8
#   s/p          char[]           bytes

# Structs can be written fully without space or everything divided by space EXCEPT a number-format couple, do NOT seperate
# 7H <=> HHHHHHH 


#  import sys !!!
#  import struct 
# in_/out_/reply_packer = struct.Struct("6s 8s 7s")
#  decode.strip('\x00')
#  UDP servernél a recvfrom-nál! rep, _ = recv



# #1 type
# Ide kerül az 1. feladat megoldása, ezzel a fájlnévvel:
#   client.py        indítás: python client.py <host> <port>   (a tesztszerver: localhost 20001)
# Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
#   python tests.py check <KÓD> feladat1        (a <KÓD> a feladat Moodle kérdésében szerepel)
# A kliens minden adatot parancssori paraméterként kap (sys.argv), input() nélkül.

import socket
import sys
import struct

sendPacker = struct.Struct("6s 8s 7s")  
replyPacker = struct.Struct("i 10s")
bookID = struct.Struct("12s")

neptun = "_".encode()
searched = "_".encode() 

server_addr = (sys.argv[1], int(sys.argv[2]))   # place, port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:   
    client.connect(server_addr)
    client.sendall(sendPacker.pack(neptun, searched, "request".encode()))
    data = client.recv(128)
    seats, classOf = replyPacker.unpack(data)
    if classOf.decode().strip('\x00') != "business" or int(seats) < 1:  # arra csere ami kell
        client.sendall(sendPacker.pack(neptun, searched, "reject".encode()))
    else:
        client.sendall(sendPacker.pack(neptun, searched, "reserve".encode()))
    data = client.recv(128)
    response = bookID.unpack(data)
    print(response[0])



# #2 type
#  Ide kerül a 2. feladat megoldása, ezzel a fájlnévvel:
#    server.py        indítás: python server.py <port>
#  Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
#    python tests.py check <KÓD> feladat2        (a <KÓD> a feladat Moodle kérdésében szerepel)
#  A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.


import select
import socket
import struct
import sys

ADDR = ("localhost", int(sys.argv[1]))
requestPacker = struct.Struct("3s 6s 8s i")
responsePacker = struct.Struct("i")

storage = {}
#{
#    "storagename": {
#        "thing": 1,
#    },
#}

def addToStorage(where, what, amt):
    if storage.get(where) == None:
        storage[where] = {}
    if storage[where].get(what) == None:
        storage[where][what] = 0
    storage[where][what] += amt
    return storage[where][what]

def getAll(where):
    summ = 0
    checked = storage[where]
    for amt in checked.values():
        summ += amt
    return summ

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(ADDR)
    server.listen(5)
    server.settimeout(1.0)
    inputs = [server]
    while True:
        readables, _, _ = select.select(inputs, [], [], 1.0)
        for s in readables:
            if s is server:  # új kliens csatlakozik, a szerver csak idáig megy a continue miatt
                client, addr = server.accept()
                inputs.append(client)
                print("Új kliens:", addr)
                continue
            req = s.recv(128)
            if not req:  # b"" -> a kliens bontotta a kapcsolatot
                print("Egy kliens bontott")
                s.close()
                inputs.remove(s)
                continue
            command, where, what, amt = requestPacker.unpack(req)
            command = command.decode().strip('\x00')
            where = where.decode().strip('\x00')
            what = what.decode().strip('\x00')
            if command == "ADD":
                resp = addToStorage(where, what, amt)
            elif command == "GET":
                resp = storage[where][what]
            elif command == "TOT":
                resp = getAll(where)
            s.sendall(responsePacker.pack(resp))


# #3 type 
# Ide kerül a 3. feladat megoldása, ezzel a fájlnévvel: 
#   proxy.py         indítás: python proxy.py <port> <szerver_port>       (az azonosítási szerver: UDP 20002)
# Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
#   python tests.py check <KÓD> feladat3        (a <KÓD> a feladat Moodle kérdésében szerepel)
# A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.

import select
import socket
import struct
import sys

PROXY_ADDR = ("localhost", int(sys.argv[1]))
SERVER_ADDR = ("localhost", int(sys.argv[2]))

requestPacker = struct.Struct("i 20s")
toServerPacker = struct.Struct("5s 20s")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as backend, socket.socket(
    socket.AF_INET, socket.SOCK_STREAM) as server:
    backend.connect(SERVER_ADDR)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(PROXY_ADDR)
    server.listen(5)
    inputs = [server]
    while True:
        readables, _, _ = select.select(inputs, [], [], 1.0)
        for s in readables:
            if s is server:
                client, addr = server.accept()
                inputs.append(client)
                continue
            msg = s.recv(128)
            if not msg:
                inputs.remove(s)
                s.close()
                continue
            loginType, name = requestPacker.unpack(msg)
            name = name.decode().strip('\x00')
            if loginType == 0:
                backend.sendto(toServerPacker.pack("LOGIN".encode(), name.encode()), SERVER_ADDR)
            elif loginType == 1:
                backend.sendto(toServerPacker.pack("GUEST".encode(), name.encode()), SERVER_ADDR)
            rep, _ = backend.recvfrom(128)
            s.sendall(rep)