#!/usr/bin/env python3
"""
simple_scanner.py - TCP connect port scanner with timestamps
"""

import socket
import sys
import datetime

ALLOWED = {"127.0.0.1", "localhost", "scanme.nmap.org"}

def ts() -> str:
    return datetime.datetime.now().isoformat(sep=' ', timespec='seconds')

def log(msg: str):
    print(f"{ts()}  {msg}", flush=True)

def scan_port(host, port, timeout=0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except Exception:
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 simple_scanner.py <host> <start_port> [end_port]")
        sys.exit(1)

    host = sys.argv[1]
    if host not in ALLOWED:
        print("ERROR: Host not authorized.")
        sys.exit(2)

    start = int(sys.argv[2])
    end = int(sys.argv[3]) if len(sys.argv) > 3 else start
    log(f"Scanning {host} ports {start}-{end}")

    for p in range(start, end + 1):
        status = "OPEN" if scan_port(host, p) else "closed"
        log(f"{host}:{p} -> {status}")

if __name__ == "__main__":
    main()
