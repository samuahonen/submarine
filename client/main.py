import socket
import keyboard  # pip install keyboard
import time

HOST = '169.254.1.1'  # Server's Ethernet IP
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to server {HOST}:{PORT}")
    
    while True:
        if keyboard.is_pressed('up'):
            s.sendall(b'UP')
            time.sleep(0.1)
        elif keyboard.is_pressed('down'):
            s.sendall(b'DOWN')
            time.sleep(0.1)
        elif keyboard.is_pressed('left'):
            s.sendall(b'LEFT')
            time.sleep(0.1)
        elif keyboard.is_pressed('right'):
            s.sendall(b'RIGHT')
            time.sleep(0.1)
