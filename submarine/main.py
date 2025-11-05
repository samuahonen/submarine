import socket
import RPi.GPIO as GPIO
import time
from motors import MotorsController


HOST = '10.100.33.146'  # your Pi’s Ethernet IP
PORT = 5001

# --- SERVER SETUP ---
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        print("Arming ESC...")
        motors = MotorsController()
        time.sleep(5)
        print("ESC armed and ready!")

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Client disconnected")
                    break

                command = data.decode().strip().upper()

                if command == "UP":
                    print("Motor Forward")
                    motors.forward()
                elif command == "DOWN":
                    print("Motor Stop")
                    motors.stop()
                elif command == "LEFT":
                    print("Motor Left")
                    motors.left()
                elif command == "RIGHT":
                    print("Motor Right")
                    motors.right()

                print(f"Client command: {command}")

            except ConnectionResetError:
                print("Client disconnected unexpectedly")
                break
            except KeyboardInterrupt:
                break

motors.stop()
