#!/usr/bin/env python3
import socket
import json
import time

HOST = "127.0.0.1"
PORT = 12346

def handle_client(conn):
    try:
        data = conn.recv(1024).decode().strip()
    except:
        data = ""
    if data == "/status":
        resp = json.dumps({
            "state": "ready",
            "color": "green",
            "text": "Сервер готов к работе"
        })
    elif data == "/generate":
        resp = "Запускаю генерацию... (имитация)"
    else:
        resp = f"Получена команда: {data}"
    conn.sendall(resp.encode())
    conn.close()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[+] Основной скрипт слушает на {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                handle_client(conn)

if __name__ == "__main__":
    run_server()
