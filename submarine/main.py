import socket
import RPi.GPIO as GPIO
import time

# --- GPIO SETUP ---
GPIO.setmode(GPIO.BCM)
ESC_PIN = 18  # PWM-capable pin
GPIO.setup(ESC_PIN, GPIO.OUT)

# 50 Hz PWM (20 ms period)
pwm = GPIO.PWM(ESC_PIN, 50)
pwm.start(0)

HOST = '10.100.33.146'  # your Pi’s Ethernet IP
PORT = 5001

def set_throttle(ms):
    """
    Set ESC throttle using pulse width in milliseconds (1.0–2.0 ms typical).
    """
    # Convert ms (1–2 ms) to duty cycle percentage
    # 1 ms  -> 5%
    # 2 ms  -> 10%
    duty = (ms / 20.0) * 100.0
    pwm.ChangeDutyCycle(duty)
    print(f"Throttle set to {ms:.2f} ms ({duty:.1f}% duty)")

# --- SERVER SETUP ---
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        # Initialize / arm ESC
        print("Arming ESC...")
        set_throttle(1.0)
        time.sleep(3)
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
                    set_throttle(2.0)
                elif command == "DOWN":
                    print("Motor Stop")
                    set_throttle(1.0)
                elif command == "REVERSE":
                    print("Motor Reverse")
                    set_throttle(0.9)

                print(f"Client command: {command}")

            except ConnectionResetError:
                print("Client disconnected unexpectedly")
                break
            except KeyboardInterrupt:
                break

# --- CLEANUP ---
pwm.stop()
GPIO.cleanup()
print("GPIO cleaned up. Server stopped.")
