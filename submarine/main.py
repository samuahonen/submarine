import socket
from gpiozero import PWMOutputDevice
import time

# Setup PWM for ESC
esc = PWMOutputDevice(pin=18, active_high=True, initial_value=0, frequency=50)

HOST = '10.100.39.149'
PORT = 5001

def set_throttle(ms):
    duty = ms / 20.0  # Convert pulse width (ms) to 20ms period duty
    esc.value = duty
    print(f"Throttle set to {ms:.2f} ms ({duty*100:.1f}% duty)")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        # Initialize / arm ESC
        set_throttle(1.0)
        time.sleep(3)
        print("ESC armed and ready")

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Client disconnected")
                    break
                command = data.decode().strip().upper()

                if command == "UP":
                    print("Motor Forward")
                    set_throttle(2.0)
                elif command == "DOWN":
                    print("Motor Stop")
                    set_throttle(1.0)
                elif command == "REVERSE":
                    print("Motor Reverse")
                    set_throttle(0.9)  # only if ESC supports reverse

                print(f"Client command: {command}")

            except ConnectionResetError:
                print("Client disconnected unexpectedly")
                break
