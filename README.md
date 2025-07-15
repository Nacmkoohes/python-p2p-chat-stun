# 🌐 P2P Chat System with STUN (Python)

A simple but complete peer-to-peer chat system using TCP sockets and a Redis-powered STUN server.

## 🔧 Features

- Real-time TCP communication between peers
- STUN server with HTTP API to register & fetch peer IP/port
- Simple terminal-based chat client/server
- Redis used for storing peer information
- Designed as a Computer Networks university project

## 📂 File Structure

| File             | Description |
|------------------|-------------|
| `stun_server.py` | STUN-like server with REST API and Redis backend |
| `client.py`      | Peer chat logic: start as TCP server or connect as client |
| `CN-project.pdf` | Project instructions (Persian) |
| `README.md`      | This file |

## 🚀 How to Run

### 1. Start Redis locally:
```bash
redis-server
```

### 2. Start STUN server:
```bash
python stun_server.py
```

### 3. Start one peer as server:
```bash
python client.py --mode server --username alice --port 6000
```

### 4. Start another peer as client:
```bash
python client.py --mode client --username bob --target alice
```

Type and send messages. Type `exit` to quit.

---

## 🧠 Authors

- Mohammad Sadegh Mohammadi  
- Abolfazl Hosseini

## 📝 License

MIT – Free to use for academic purposes.


---

## ⭐ Bonus: File Transfer Support

You can send files between peers using the `client_plus.py` version:

### Example:
1. Start one peer as server:
```bash
python client_plus.py --mode server --username alice --port 6000
```

2. Start another peer as client:
```bash
python client_plus.py --mode client --username bob --target alice
```

3. To send a file from Bob to Alice:
```
file:example.txt
```

Files will be saved as `received_example.txt`.

---

## 🧪 Notes

- File sending is optional, available only in `client_plus.py`
- Ideal for final projects with bonus implementation
