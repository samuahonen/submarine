import socket
from gpiozero import PWMOutputDevice
import time
import sys

# --- ESC SETUP ---
ESC_PIN = 18  # GPIO18 → physical pin 12 on Raspberry Pi
esc = PWMOutputDevice(pin=ESC_PIN, active_high=True, initial_value=0, frequency=50)

# --- NETWORK CONFIG ---
# Detect Pi's local Ethernet IP automatically
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to actually connect; just used to get interface IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

HOST = get_local_ip()
PORT = 5001

# --- ESC FUNCTION ---
def set_throttle(ms):
    """Set ESC throttle in milliseconds (1.0–2.0 typical range)."""
    duty = ms / 20.0  # Convert pulse width to 20 ms period duty
    esc.value = duty
    print(f"Throttle set to {ms:.2f} ms  ({duty*100:.1f}% duty)")

# --- MAIN SERVER LOOP ---
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"🚀 Server listening on {HOST}:{PORT}")

        while True:
            print("🔄 Waiting for client...")
            conn, addr = s.accept()
            with conn:
                print(f"✅ Connected by {addr}")
                try:
                    # Arm ESC
                    set_throttle(1.0)
                    time.sleep(3)
                    print("ESC armed and ready")

                    while True:
                        data = conn.recv(1024)
                        if not data:
                            print("Client disconnected")
                            break

                        command = data.decode().strip().upper()

                        if command == "UP":
                            print("Motor → FORWARD")
                            set_throttle(2.0)
                        elif command == "DOWN":
                            print("Motor → STOP")
                            set_throttle(1.0)
                        elif command == "REVERSE":
                            print("Motor → REVERSE")
                            set_throttle(0.9)
                        elif command == "EXIT":
                            print("🔌 Shutting down server...")
                            set_throttle(1.0)
                            sys.exit(0)
                        else:
                            print(f"Unknown command: {command}")

                except ConnectionResetError:
                    print("⚠️ Client disconnected unexpectedly")
                finally:
                    # Safety stop on disconnect
                    set_throttle(1.0)
                    print("ESC set to safe state\n")

if __name__ == "__main__":
    start_server()
