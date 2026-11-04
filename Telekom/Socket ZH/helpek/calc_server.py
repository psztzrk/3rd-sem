import socket
import struct
import sys
import select

def recv_exact(sock, size):
    """Addig olvas, amíg pontosan size byte meg nem érkezik (vagy a másik oldal bont)."""
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data

packer = struct.Struct("i i c")  # ket szam es a muveleti jel
ops = {
    b"+": lambda a, b: a + b,
    b"-": lambda a, b: a - b,
    b"*": lambda a, b: a * b,
    b"/": lambda a, b: a // b,
}
server_addr = ("", int(sys.argv[1]))  # pl. python calc_server.py 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_addr)
    sock.listen(1)
    sock.settimeout(1.0)  # Windowson a Ctrl+C csak igy szakitja meg az accept-et

    try:
        inputs = [sock]
        while True:
            readables, _, _ = select.select(inputs, [], [], 1.0)
            for s in readables:
                if s is sock:  # új kliens csatlakozik
                    client, addr = sock.accept()
                    inputs.append(client)
                    print("Új kliens:", addr)
                    continue
                # time.sleep(1)                             # [K6] a szerver lassú: vár egy kicsit olvasás előtt
                #msg = s.recv(1024)  # [K7] javításnál ezt kommenteld ki...
                msg = recv_exact(s, packer.size)          # [K7] ...és ezt kapcsold be: a teljes 9 byte-ot várjuk meg
                if not msg:  # b"" -> a kliens bontotta a kapcsolatot
                    print("Egy kliens bontott")
                    s.close()
                    inputs.remove(s)  # [K5] tedd kommentbe ezt a sort!
                    continue
                else:
                    a, b, op = packer.unpack(msg)
                    result = ops[op](a, b)
                    print(f"{a} {op.decode()} {b} = {result}")
                    s.sendall(packer.pack(result, 0, b"R"))

    except KeyboardInterrupt:
        print("Server stopped")
