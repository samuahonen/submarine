import socket
import pigpio
import time

# --- ESC SETUP ---
ESC_PIN = 18
pi = pigpio.pi()
if not pi.connected:
    raise SystemExit("❌ Cannot connect to pigpio daemon. Run 'sudo pigpiod' first!")

HOST = '10.100.33.146'
PORT = 5001

# ESC expects pulse widths between ~1000 µs (min) and ~2000 µs (max)
def set_throttle(ms):
    pulse_width = int(ms * 1000)  # convert ms → µs
    pi.set_servo_pulsewidth(ESC_PIN, pulse_width)
    print(f"Throttle set to {ms:.2f} ms ({pulse_width} µs)")

# --- MAIN SERVER ---
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"🚀 Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    with conn:
        print(f"✅ Connected by {addr}")

        # Initialize / Arm ESC
        set_throttle(1.5)
        time.sleep(2)
        print("ESC armed and ready")

        while True:
            try:
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
                    set_throttle(1.5)
                elif command == "REVERSE":
                    print("Motor → REVERSE")
                    set_throttle(1.0)
                
                print(f"Client command: {command}")
                
            except ConnectionResetError:
                print("⚠️ Client disconnected unexpectedly")
                break
            except KeyboardInterrupt:
                break

# Stop the ESC safely
set_throttle(0)
pi.stop()
print("🛑 ESC signal stopped, pigpio released")
