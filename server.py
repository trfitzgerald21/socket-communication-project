#!/usr/bin/env python3
"""
server.py - simple timestamped TCP server (single client)
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

def start_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen(1)
            log(f"[+] Server listening on {HOST}:{PORT} ...")

            conn, addr = s.accept()
            with conn:
                log(f"[+] Connected by: {addr}")
                while True:
                    data = conn.recv(BUFFER)
                    if not data:
                        log("[+] Client closed connection.")
                        break
                    msg = data.decode('utf-8', errors='replace')
                    log(f"[Client] -> {msg!r}")
                    reply = f"Server received: {msg}"
                    conn.sendall(reply.encode('utf-8'))
    except KeyboardInterrupt:
        log("[!] Server shutting down gracefully.")
        sys.exit(0)
    except Exception as e:
        log(f"[ERROR] Unexpected: {type(e).__name__}: {e}")
        sys.exit(2)

if __name__ == "__main__":
    start_server()
