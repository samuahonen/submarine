import socket
from gpiozero import LED


led = LED(18)  # Pin 18 (GPIO18)
HOST = '10.100.39.149'  # Server's Ethernet IP
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Client disconnected")
                    break
                command = data.decode()
                if command == "UP":
                    led.on()
                if command == "DOWN":
                    led.off()
                print(f"Client command: {command}")
            except ConnectionResetError:
                print("Client disconnected unexpectedly")
                break
