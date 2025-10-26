#!/usr/bin/env python3
"""
client.py - timestamped TCP client
"""

import socket
import datetime
import sys

HOST = "127.0.0.1"
PORT = 5000
BUFFER = 1024

def ts() -> str:
    return datetime.datetime.now().isoformat(sep=' ', timespec='seconds')

def log(msg: str):
    print(f"{ts()}  {msg}", flush=True)

def start_client(message: str = "Hello from the client!"):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            log(f"[+] Attempting connection to {HOST}:{PORT} ...")
            s.connect((HOST, PORT))
            log("[+] Connected to server.")
            s.sendall(message.encode('utf-8'))
            log(f"[Sent] -> {message!r}")
            response = s.recv(BUFFER).decode('utf-8', errors='replace')
            log(f"[Received] <- {response!r}")
            log("[+] Client disconnecting cleanly.")
    except ConnectionRefusedError:
        log("[ERROR] Connection refused - server may not be running.")
        sys.exit(3)
    except socket.timeout:
        log("[ERROR] Connection timed out.")
        sys.exit(4)
    except Exception as e:
        log(f"[ERROR] Unexpected: {type(e).__name__}: {e}")
        sys.exit(2)

if __name__ == "__main__":
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello from the client!"
    start_client(message)
