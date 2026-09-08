#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import json
import sys

HOST = '127.0.0.1'
PORT = 12346

def handle_connection(conn):
    try:
        data = conn.recv(4096).decode('utf-8').strip()
    except:
        data = ''

    if data == '/status':
        answer = {
            'state': 'online',
            'color': 'green',
            'text': 'Сервер готов к диффузии'
        }
        response = json.dumps(answer, ensure_ascii=False)
    elif data == '/generate':
        response = 'Запуск генерации... (имитация)'
    elif data == '/hello':
        response = 'Привет от основного скрипта!'
    else:
        response = f'Неизвестная команда: {data}'

    conn.sendall(response.encode('utf-8'))
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f'[main] Слушаю {HOST}:{PORT}')
        while True:
            conn, addr = s.accept()
            with conn:
                handle_connection(conn)

if __name__ == '__main__':
    main()
