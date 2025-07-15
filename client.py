import socket
import threading
import requests

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if data:
                print("\n[Peer] " + data)
            else:
                break
        except:
            break

def start_client(username, target_username):
    # Step 1: get peer info
    res = requests.get(f"http://localhost:5000/peerinfo", params={'username': target_username})
    if res.status_code != 200:
        print("Could not retrieve peer info.")
        return
    peer_address = res.json()['address']
    peer_ip, peer_port = peer_address.split(':')

    # Step 2: connect to peer
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((peer_ip, int(peer_port)))
    print(f"[Connected to {target_username} at {peer_ip}:{peer_port}]")

    # Step 3: start listener
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # Step 4: send messages
    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        sock.send(msg.encode())

def start_server(username, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    print(f"[Listening on port {port}]")

    # Register to STUN server
    requests.post("http://localhost:5000/register", params={'username': username, 'IP': '127.0.0.1', 'PORT': port})

    def handle_client(conn, addr):
        print(f"[Peer connected from {addr}]")
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print("\n[Peer] " + data)
            except:
                break
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
    parser.add_argument('--target', help="Username of the peer to connect to (for client mode only)")
    args = parser.parse_args()

    if args.mode == 'server':
        if not args.port:
            print("Please specify --port for server mode.")
        else:
            start_server(args.username, args.port)
    else:
        if not args.target:
            print("Please specify --target for client mode.")
        else:
            start_client(args.username, args.target)
