import socket
import threading
import requests
import os

BUFFER_SIZE = 1024

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            if data.startswith(b"[FILE]"):
                filename = data.decode().split(":", 1)[1]
                with open("received_" + filename, "wb") as f:
                    while True:
                        chunk = sock.recv(BUFFER_SIZE)
                        if chunk == b"<END>":
                            break
                        f.write(chunk)
                    print(f"[File received] saved as received_{filename}")
            else:
                print("\n[Peer] " + data.decode())
        except:
            break

def send_file(sock, filepath):
    if not os.path.exists(filepath):
        print("File not found.")
        return
    sock.send(f"[FILE]:{os.path.basename(filepath)}".encode())
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break
            sock.send(chunk)
    sock.send(b"<END>")
    print("[File sent]")

def start_client(username, target_username):
    res = requests.get("http://localhost:5000/peerinfo", params={'username': target_username})
    if res.status_code != 200:
        print("Could not retrieve peer info.")
        return
    peer_address = res.json()['address']
    peer_ip, peer_port = peer_address.split(':')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((peer_ip, int(peer_port)))
    print(f"[Connected to {target_username} at {peer_ip}:{peer_port}]")

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        elif msg.startswith("file:"):
            filepath = msg[5:].strip()
            send_file(sock, filepath)
        else:
            sock.send(msg.encode())

def start_server(username, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    print(f"[Listening on port {port}]")

    requests.post("http://localhost:5000/register", params={'username': username, 'IP': '127.0.0.1', 'PORT': port})

    def handle_client(conn, addr):
        print(f"[Peer connected from {addr}]")
        receive_messages(conn)
        conn.close()

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['server', 'client'], required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--port', type=int)
    parser.add_argument('--target', help="Target peer username for client mode")
    args = parser.parse_args()

    if args.mode == 'server':
        if not args.port:
            print("Please provide --port for server mode.")
        else:
            start_server(args.username, args.port)
    else:
        if not args.target:
            print("Please provide --target for client mode.")
        else:
            start_client(args.username, args.target)
