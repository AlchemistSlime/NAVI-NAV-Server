#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import json

HOST = '127.0.0.1'
PORT = 12345

COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[0m'
}

def colorize(text, color='white'):
    return f'{COLORS.get(color, "")}{text}{COLORS["reset"]}'

def send_command(cmd):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((HOST, PORT))
            sock.sendall(cmd.encode('utf-8'))
            resp = sock.recv(4096).decode('utf-8')
            return resp
    except socket.timeout:
        return colorize('Таймаут соединения', 'red')
    except ConnectionRefusedError:
        return colorize('Загрузчик не запущен или порт занят.', 'red')
    except Exception as e:
        return colorize(f'Ошибка: {e}', 'red')

def show_help():
    print(colorize('Доступные команды для загрузчика (через /p):', 'yellow'))
    print('  /p reload     – обновить основной скрипт из GitHub и перезапустить')
    print('  /p stop       – остановить загрузчик')
    print('  /p notepad    – открыть Блокнот (можно добавить текст через пробел)')
    print('  /p status     – статус основного скрипта (загрузчик)')
    print(colorize('\nОстальные команды проксируются на основной скрипт:', 'yellow'))
    print('  /status       – статус основного скрипта')
    print('  /generate     – имитация генерации')
    print('  /hello        – приветствие от основного скрипта')

def main():
    print(colorize('=== Интерактивный клиент для Diffusers ===', 'cyan'))
    print('Команды с /p отправляются загрузчику, остальные – прокси на основной скрипт.')
    print('Введите exit для выхода, help для справки.\n')

    while True:
        try:
            cmd = input(colorize('> ', 'blue')).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not cmd:
            continue
        if cmd.lower() == 'exit':
            break
        if cmd.lower() == 'help':
            show_help()
            continue

        resp = send_command(cmd)

        # Если ответ — JSON, пробуем вывести цветной статус
        if resp.startswith('{') and resp.endswith('}'):
            try:
                data = json.loads(resp)
                if 'state' in data and 'color' in data:
                    print(colorize(f"[{data['state']}] {data.get('text', '')}", data['color']))
                    continue
            except:
                pass

        print(resp)

if __name__ == '__main__':
    main()
