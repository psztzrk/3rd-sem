import select
import socket
import struct
import time

ADDR = ("localhost", 10000)
SERVER_ADDR = ("localhost", 10001)
packer = struct.Struct(
    "i i c"
)  # a [K7] kísérlet üzenete: két szám és egy műveleti jel, 9 byte
udp_packer = struct.Struct(
    "i i c"
)

def recv_exact(sock, size):
    """Addig olvas, amíg pontosan size byte meg nem érkezik (vagy a másik oldal bont)."""
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def select_server():
    """Egyszerre több klienssel foglalkozik: a select megmondja, melyik socketen van teendő."""
    with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server,
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock):

        server.bind(ADDR)
        server.listen(5)
        print("Select szerver fut:", ADDR)
        inputs = [server]
        while True:
            readables, _, _ = select.select(inputs, [], [], 1.0)
            for client_sock in readables:
                if client_sock is server:  # új kliens csatlakozik
                    client, addr = server.accept()
                    inputs.append(client)
                    print("Új kliens:", addr)
                    continue

                msg = recv_exact(client_sock, packer.size)
                if not msg:  # b"" -> a kliens bontotta a kapcsolatot
                    print("Egy kliens bontott")
                    client_sock.close()
                    inputs.remove(client_sock)
                    continue
                else:
                    # forward to server
                    unpacked_msg = packer.unpack(msg)
                    print(unpacked_msg)
                    packed_msg = udp_packer.pack(*unpacked_msg)

                    udp_sock.sendto(packed_msg, SERVER_ADDR)
                    data, server_address = udp_sock.recvfrom(packer.size)
                    client_sock.sendall(data)



if __name__ == "__main__":
    select_server()  # [K4]-[K7]
