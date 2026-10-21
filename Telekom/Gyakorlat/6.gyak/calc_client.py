import socket
import struct
import sys
import time

packer = struct.Struct("i i c")  # ket szam es a muveleti jel
# pl. python calc_client.py localhost 10000 6 x 7   (a szorzas jele itt x, mert a * a shellben mast jelent)
host, port, a, op, b = (
    sys.argv[1],
    int(sys.argv[2]),
    int(sys.argv[3]),
    sys.argv[4],
    int(sys.argv[5]),
)
op = "*" if op == "x" else op

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))
    msg = packer.pack(a, b, op.encode())
    client.sendall(msg[:1])
    time.sleep(2)
    client.sendall(msg[1:2])
    time.sleep(2)
    client.sendall(msg[2:3])
    time.sleep(2)
    client.sendall(msg[3:4])
    time.sleep(2)
    client.sendall(msg[4:])
    result, _, _ = packer.unpack(client.recv(packer.size))
    print(f"{a} {op} {b} = {result}")
