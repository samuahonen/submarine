import socket
from gpiozero import PWMOutputDevice
import time

# Setup PWM for ESC
esc = PWMOutputDevice(pin=18, active_high=True, initial_value=0, frequency=50)

HOST = '10.100.39.149'
PORT = 5001

def set_throttle(ms):
    duty = (ms - 1.0) / 1.0  # 1ms -> 0, 2ms -> 1
    esc.value = duty
    print(f"Throttle set to {ms} ms ({duty:.2f})")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        # Initialize ESC
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
                    set_throttle(2.0)
                elif command == "DOWN":
                    print("Motor Stop")
                    set_throttle(1.5)
                elif command == "REVERSE":
                    print("Motor Reverse")
                    set_throttle(1.0)
                
                print(f"Client command: {command}")
                
            except ConnectionResetError:
                print("Client disconnected unexpectedly")
                break
