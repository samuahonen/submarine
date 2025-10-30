import socket
from gpiozero import PWMOutputDevice
import time

# Setup PWM on GPIO18 for ESC
esc = PWMOutputDevice(18, True, 0, 50)  # 50 Hz typical for ESC

HOST = '10.100.39.149'  # Server's Ethernet IP
PORT = 5001

# Function to set throttle in ms
def set_throttle(ms):
    duty = ms / 20.0 * 100  # convert 1-2 ms to duty cycle %
    esc.value = duty / 100.0  # gpiozero PWM expects 0..1
    print(f"Throttle set to {ms} ms ({duty:.2f}%)")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        # Initialize ESC (throttle to neutral / stop)
        set_throttle(1.5)
        time.sleep(2)
        
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Client disconnected")
                    break
                command = data.decode().strip()
                
                if command == "UP":
                    print("Motor Forward")
                    set_throttle(2.0)  # full forward
                elif command == "DOWN":
                    print("Motor Stop")
                    set_throttle(1.5)  # stop / neutral
                elif command == "REVERSE":
                    print("Motor Reverse")
                    set_throttle(1.0)  # optional reverse if ESC supports it
                
                print(f"Client command: {command}")
                
            except ConnectionResetError:
                print("Client disconnected unexpectedly")
                break
