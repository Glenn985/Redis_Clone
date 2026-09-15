import socket
import time

HOST = "127.0.0.1"
PORT = 45123

N = 10000

connections = []


def recv_line(sock):
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def one_client(i):
    try:
        sock = socket.create_connection((HOST, PORT))
        connections.append(sock)
        sock.sendall(f"SET key{i} value{i}\n".encode())
        response = recv_line(sock)
        sock.sendall(f"GET key{i}\n".encode())
        response = recv_line(sock)

        # DON'T CLOSE HERE
        # Keep connection open

        return True

    except Exception as e:
        print("FAILED:", i, e)
        return False


def main():
    start = time.perf_counter()

    results = []

    for i in range(N):
        results.append(one_client(i))

    end = time.perf_counter()

    successful = sum(results)
    failed = N - successful

    print("Successful:", successful)
    print("Failed:", failed)
    print("Time:", end - start)

    print("Connections being held open:", len(connections))
    # Keep all connections alive for 60 seconds
    time.sleep(60)
    # Close them afterwards
    for sock in connections:
        try:
            sock.close()
        except Exception:
            pass
    print("All connections closed.")
if __name__ == "__main__":
    main()